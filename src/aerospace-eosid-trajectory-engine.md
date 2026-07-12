```python
# Antony Duran
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
```

# Autonomous EOSID Trajectory Generation with Google ADK

**_NOTE_**: This notebook has been tested in the following environment:

* Python version = 3.10.13

## Overview

This tutorial demonstrates how to define a collaborative multi-agent trajectory calculation pattern for Engine Out Standard Instrument Departures (EOSID) using the Google Agent Development Kit (ADK) and Vertex AI (Gemini).

In aviation, standard departure paths assume all engines are functional. If an engine fails, the aircraft's climb capability is significantly reduced. An EOSID is a custom departure procedure designed to guide the aircraft safely through mountainous terrain or around obstacles. Calculating these trajectories typically involves analyzing terrain heights, runway headings, and climb performance curves.

In this notebook, we use the Google Agent Development Kit (ADK) to build two cooperative agents:
1. **TrajectoryPlannerAgent**: A reasoning agent that proposes headings and climbs.
2. **ObstacleVerifierAgent**: A validating agent that cross-checks proposed paths against terrain heights and OEI physics.

> **Safety notice:** This is an educational simulation using synthetic terrain and simplified performance equations.
> It is not suitable for flight planning, aircraft operation, or regulatory compliance.

### Objective

In this tutorial, you learn how to configure ADK agent definitions and execute a deterministic planner-verifier simulation for a safety-critical pathfinding example.

This tutorial uses the following Google Cloud ML services and resources:

- **Vertex AI (Gemini 1.5 Flash)**: Core reasoning model.
- **Google Agent Development Kit (ADK)**: Python SDK for multi-agent coordination.

The steps performed include:

- Define a physics model for One-Engine-Inoperative (OEI) climb profiles.
- Define a mountainous airport obstacle database.
- Define ADK tools for segment clearance calculation.
- Configure `TrajectoryPlannerAgent` and `ObstacleVerifierAgent` definitions using Google ADK.
- Run a deterministic planner-verifier loop to resolve a simulated takeoff path.
- Visualize the negotiated 3D trajectory path against terrain using matplotlib.

### Dataset

This tutorial uses self-contained aircraft performance parameters and obstacle coordinates representing a challenging takeoff from Innsbruck (LOWI) Runway 26.
- **Aircraft specs**: Twin-engine commercial passenger jet with one engine inoperative (OEI). Climb gradient is modeled as a function of thrust loss, speed, weight, drag, and lift.
- **Terrain database**: Mock terrain points representing the surrounding Alpine valley ridges.

### Costs

This tutorial uses billable components of Google Cloud:

* Vertex AI (Gemini API)

Learn about [Vertex AI pricing](https://cloud.google.com/vertex-ai/pricing) and use the [Pricing Calculator](https://cloud.google.com/products/calculator/) to generate a cost estimate based on your projected usage.

## Installation

Install the following packages required to execute this notebook. 

We recommend using the latest major version of each package (i.e. --upgrade).

```python
! pip3 install --upgrade --quiet google-adk google-cloud-aiplatform matplotlib
```

## Before you begin

### Set up your Google Cloud project

**The following steps are required, regardless of your notebook environment.**

1. [Select or create a Google Cloud project](https://console.cloud.google.com/cloud-resource-manager). When you first create an account, you get a $300 free credit towards your compute/storage costs.

2. [Make sure that billing is enabled for your project](https://cloud.google.com/billing/docs/how-to/modify-project).

3. [Enable the Vertex AI API](https://console.cloud.google.com/flows/enableapi?apiid=aiplatform.googleapis.com).

4. If you are running this notebook locally, you need to install the [Cloud SDK](https://cloud.google.com/sdk).

#### Set your project ID

**If you don't know your project ID**, try the following:
* Run `gcloud config list`.
* Run `gcloud projects list`.
* See the support page: [Locate the project ID](https://support.google.com/googleapi/answer/7014113)

```python
GOOGLE_CLOUD_PROJECT = ""  # @param {type:"string"}

if not GOOGLE_CLOUD_PROJECT:
    raise ValueError("Set GOOGLE_CLOUD_PROJECT before running the notebook.")

# Set the project id
if GOOGLE_CLOUD_PROJECT:
    ! gcloud config set project {GOOGLE_CLOUD_PROJECT}
```

#### Region

You can also change the `GOOGLE_CLOUD_LOCATION` variable used by Vertex AI. Learn more about [Vertex AI regions](https://cloud.google.com/vertex-ai/docs/general/locations).

```python
GOOGLE_CLOUD_LOCATION = "us-central1"  # @param {type:"string"}
```

### Authenticate your Google Cloud account

The Cloud SDK, code and other libraries currently run as the service account identity of the Workbench Instance running this notebook.

**- Authenticate the Cloud SDK with your credentials :**

```python
# ! gcloud auth login
```

**- Authenticate code and libraries with your credentials :**

```python
# ! gcloud auth application-default
```

**- Service account or other**
* See how to grant Cloud Storage permissions to your service account at https://cloud.google.com/storage/docs/gsutil/commands/iam#ch-examples.

### Create a Cloud Storage bucket

Create a storage bucket to store intermediate artifacts such as datasets.
The generated name includes the project ID to reduce collisions; replace it if your organization requires a different naming convention.

```python
BUCKET_URI = f"gs://aerospace-eosid-{GOOGLE_CLOUD_PROJECT}-unique"  # @param {type:"string"}
```

**Only if your bucket doesn't already exist**: Run the following cell to create your Cloud Storage bucket.

```python
! gsutil mb -l {GOOGLE_CLOUD_LOCATION} -p {GOOGLE_CLOUD_PROJECT} {BUCKET_URI}
```

### Import libraries

```python
import asyncio
import math
import os
from google.cloud import aiplatform
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import matplotlib.pyplot as plt
```

### Initialize Vertex AI SDK for Python

Initialize the Vertex AI SDK for Python for your project.

```python
# ADK reads these standard variables to select Vertex AI instead of an API key.
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
os.environ["GOOGLE_CLOUD_PROJECT"] = GOOGLE_CLOUD_PROJECT
os.environ["GOOGLE_CLOUD_LOCATION"] = GOOGLE_CLOUD_LOCATION

aiplatform.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION, staging_bucket=BUCKET_URI)
```

## Physics and Airport Obstacle Database

Define the simplified physical calculations for OEI (One-Engine-Inoperative) climb profiles, and set up a mock Innsbruck (LOWI) runway and surrounding terrain obstacles database.

```python
# Simplified Flight Physics Model
# Standard commercial jet takeoff parameters
AIRCRAFT_SPECS = {
    "weight_kg": 75000,
    "thrust_n_per_engine": 120000,
    "oei_thrust_n": 120000,  # One engine remains operative.
    "drag_coefficient_cd": 0.045,
    "lift_to_drag_ratio": 12.0,
    "takeoff_speed_mps": 75.0,  # Approximately 145 knots.
    "climb_gradient_min": 0.024,  # Simplified 2.4% OEI minimum gradient.
}

def calculate_oei_climb_angle(weight_kg, thrust_n, lift_to_drag_ratio):
    """Return the simplified OEI climb gradient and angle in radians."""
    g = 9.81
    weight_force_n = weight_kg * g
    climb_gradient = (thrust_n / weight_force_n) - (1.0 / lift_to_drag_ratio)
    if not 0 < climb_gradient < 1:
        raise ValueError("The simplified OEI climb gradient must be between zero and one.")
    climb_angle_rad = math.asin(climb_gradient)
    return climb_gradient, climb_angle_rad

# Innsbruck (LOWI) Runway 26 Mock Terrain peaks
# X represents distance along runway centerline (meters), Y is lateral deviation (meters), Z is height (meters)
OBSTACLE_DATABASE = [
    {"name": "Martinswand Peak", "x": 5000, "y": 800, "z": 850},
    {"name": "Kranebitten Ridge", "x": 3000, "y": -400, "z": 450},
    {"name": "Volderberg Peak", "x": 10000, "y": -1200, "z": 1200},
    {"name": "Zirl Spur", "x": 8000, "y": 1500, "z": 1050},
    {"name": "Kematen Ridge", "x": 6000, "y": -900, "z": 700}
]

# Runway starts at (0, 0, 0)
RUNWAY_LENGTH = 2000
print("Flight physics and Airport Obstacle database initialized.")
```

## Configuring Google ADK Multi-Agent Team

We now configure two collaborative ADK agent definitions and a coordinator.
The coordinator delegates the proposal to the planner and the safety review to the verifier, which can call the deterministic clearance tool.
The later deterministic verifier remains the source of truth for the plotted path because an LLM response is not flight-safety evidence.
1. **TrajectoryPlannerAgent**: Responsible for proposing path segments (headings and target heights).
2. **ObstacleVerifierAgent**: Responsible for cross-checking the proposed segment coordinates against the obstacle database and confirming clearance.

```python
# Define tool for ObstacleVerifierAgent
def check_segment_clearance(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> str:
    """
    Validates if a flight segment from (x1, y1, z1) to (x2, y2, z2) clears all obstacles.
    Returns 'APPROVED' if the path clears all obstacles by 35 feet (10.6m) margin,
    otherwise returns 'REJECTED' with the blocking obstacle name and recommended safe altitude or turn suggestion.
    """
    safety_margin = 10.6  # 35 feet simplified obstacle clearance margin.
    # Find distance from line segment to each obstacle
    for obs in OBSTACLE_DATABASE:
        obs_x, obs_y, obs_z = obs["x"], obs["y"], obs["z"]
        # Project obstacle onto line segment to check closest point
        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        line_len_sq = dx * dx + dy * dy + dz * dz
        if line_len_sq == 0:
            continue
        
        t = ((obs_x - x1) * dx + (obs_y - y1) * dy + (obs_z - z1) * dz) / line_len_sq
        t = max(0.0, min(1.0, t))  # Clamp to the segment.
        
        closest_x = x1 + t*dx
        closest_y = y1 + t*dy
        closest_z = z1 + t*dz
        
        dist_horizontal = math.hypot(obs_x - closest_x, obs_y - closest_y)
        # The synthetic obstacles use a 500 m horizontal protected radius.
        if dist_horizontal < 500:
            if closest_z < obs_z + safety_margin:
                required_z = obs_z + safety_margin
                return (
                    f"REJECTED: Collision risk with {obs['name']} at "
                    f"(x={obs_x}, y={obs_y}, z={obs_z}). Segment height is "
                    f"{closest_z:.1f} m but must clear {required_z:.1f} m."
                )
    
    return "APPROVED"

trajectory_planner_agent = Agent(
    name="trajectory_planner",
    model="gemini-2.5-flash",
    instruction=(
        "Propose a conservative simulated EOSID segment. State its start and end "
        "coordinates in meters and identify the assumed heading. Do not claim that "
        "the result is suitable for real-world flight operations."
    ),
)
obstacle_verifier_agent = Agent(
    name="obstacle_verifier",
    model="gemini-2.5-flash",
    instruction=(
        "Review each simulated segment by calling check_segment_clearance with the "
        "segment coordinates. Reject a segment unless the tool returns APPROVED."
    ),
    tools=[check_segment_clearance],
)
eosid_coordinator_agent = Agent(
    name="eosid_coordinator",
    model="gemini-2.5-flash",
    instruction=(
        "Coordinate the trajectory_planner and obstacle_verifier agents. Ask the "
        "planner for a candidate, then ask the verifier to use its tool. Return a "
        "short simulation-only summary that includes the verifier decision."
    ),
    sub_agents=[trajectory_planner_agent, obstacle_verifier_agent],
)
print("ADK planner, verifier, coordinator, and clearance tool are prepared.")
```

## Running the ADK Trajectory Negotiation

This cell creates an in-memory ADK session and invokes `Runner.run_async()` against Vertex AI.
It exposes the actual planner-to-verifier delegation and tool-call trace in the notebook output.
Run it only after you have configured Application Default Credentials and enabled the Vertex AI API; it incurs Vertex AI usage.

```python
async def run_adk_negotiation() -> str:
    """Run one inspectable ADK planner-verifier negotiation turn."""
    app_name = "eosid_trajectory_workshop"
    user_id = "workshop_attendee"
    session_id = "eosid_negotiation"
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )
    runner = Runner(
        agent=eosid_coordinator_agent,
        app_name=app_name,
        session_service=session_service,
    )
    prompt = (
        "Simulate one EOSID proposal from (0, 0, 0) to (1500, 0, 180). "
        "Delegate the proposal and verification. The verifier must call its tool."
    )
    final_response = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"{event.author}: {part.text}")
        if event.is_final_response() and event.content and event.content.parts:
            final_response = "".join(
                part.text for part in event.content.parts if part.text
            )
    if not final_response:
        raise RuntimeError("ADK completed without a final trajectory negotiation response.")
    return final_response


adk_trajectory_summary = await run_adk_negotiation()
print(f"ADK negotiation summary: {adk_trajectory_summary}")
```

## Running the Deterministic Safety Verifier

The following independent calculation creates the visualization input.
It deliberately encounters the mock obstacle field, rejects an unsafe segment, and takes a fixed diversion so every attendee can reproduce and inspect the safety result without treating the model output as operational guidance.

```python
# Deterministic planner-verifier simulation used for the plotted educational result.
print("--- Starting Trajectory Negotiation Loop ---")

current_pos = {"x": 0.0, "y": 0.0, "z": 0.0}
trajectory_path = [tuple(current_pos.values())]
target_altitude = 1200.0  # Simulated exit altitude.
heading = 0.0  # Points toward the synthetic obstacle field.

# Twin-engine OEI Climb Performance
gradient, _ = calculate_oei_climb_angle(
    AIRCRAFT_SPECS["weight_kg"],
    AIRCRAFT_SPECS["oei_thrust_n"],
    AIRCRAFT_SPECS["lift_to_drag_ratio"]
)

print(f"OEI Climb Gradient: {gradient:.4f} ({gradient*100:.2f}%)")
if gradient < AIRCRAFT_SPECS["climb_gradient_min"]:
    raise RuntimeError("The simulated OEI climb gradient is below the configured minimum.")

segment_distance = 1500.0  # Meters per step.
max_steps = 15
step = 0

while current_pos["z"] < target_altitude and step < max_steps:
    step += 1
    rad_heading = math.radians(heading)
    next_x = current_pos["x"] + segment_distance * math.cos(rad_heading)
    next_y = current_pos["y"] + segment_distance * math.sin(rad_heading)
    next_z = current_pos["z"] + segment_distance * gradient
    
    status = check_segment_clearance(
        current_pos["x"], current_pos["y"], current_pos["z"],
        next_x, next_y, next_z
    )
    
    print(
        f"\n[Step {step}] Planner proposes: "
        f"(x={next_x:.1f}, y={next_y:.1f}, z={next_z:.1f}) on heading {heading:.1f}"
    )
    print(f"[Step {step}] Verifier response: {status}")
    
    if "APPROVED" in status:
        current_pos = {"x": next_x, "y": next_y, "z": next_z}
        trajectory_path.append(tuple(current_pos.values()))
    else:
        # The planner takes a fixed diversion after a verifier rejection.
        print("Planner: Re-routing to heading 30.0 to avoid the protected obstacle radius.")
        heading = 30.0
            
print("\nNegotiation completed. Final Trajectory Points:")
for p in trajectory_path:
    print(f"  Point: X={p[0]:.1f}, Y={p[1]:.1f}, Z={p[2]:.1f}")
```

## Trajectory and Obstacle Visualization

Finally, we plot the resolved trajectory against the obstacles in both 3D and 2D.

```python
fig = plt.figure(figsize=(14, 6))

# 3D Plot
ax = fig.add_subplot(121, projection='3d')
xs, ys, zs = zip(*trajectory_path)
ax.plot(xs, ys, zs, label='Negotiated Flight Path (OEI)', color='blue', linewidth=3, marker='o')

# Plot runway
ax.plot([0, RUNWAY_LENGTH], [0, 0], [0, 0], label='Runway 26', color='black', linewidth=4)

# Plot obstacles
for obs in OBSTACLE_DATABASE:
    ax.scatter(obs["x"], obs["y"], obs["z"], color='red', s=100, marker='^')
    ax.text(obs["x"], obs["y"], obs["z"] + 50, obs["name"], fontsize=8)
    
ax.set_xlabel('Distance from start (m)')
ax.set_ylabel('Lateral deviation (m)')
ax.set_zlabel('Altitude (m)')
ax.set_title('3D Takeoff Trajectory (LOWI)')
ax.legend()

# 2D Elevation Profile Plot
ax2 = fig.add_subplot(122)
distances = [math.sqrt(p[0]**2 + p[1]**2) for p in trajectory_path]
ax2.plot(distances, zs, label='Flight Path Altitude', color='blue', marker='o', linewidth=2)

# Draw vertical obstacle profiles
for obs in OBSTACLE_DATABASE:
    obs_dist = math.sqrt(obs["x"]**2 + obs["y"]**2)
    ax2.vlines(obs_dist, 0, obs["z"], colors='red', linestyles='dashed', alpha=0.7)
    ax2.text(obs_dist, obs["z"] + 20, obs["name"], rotation=90, verticalalignment='bottom', fontsize=8)
    
ax2.set_xlabel('Distance along path (m)')
ax2.set_ylabel('Altitude (m)')
ax2.set_title('Vertical Profile & Obstacle Clearance')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()
```

## Cleaning up

To clean up all Google Cloud resources used in this project, you can [delete the Google Cloud
project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#shutting_down_projects) you used for the tutorial.

Otherwise, you can delete the individual resources you created in this tutorial:

In this tutorial, no persistent endpoints or models were deployed.
Set `delete_bucket` to `True` only when you want to delete the bucket configured above and all of its contents.

```python
# This is intentionally opt-in because deleting a bucket is irreversible.
delete_bucket = False  # @param {type:"boolean"}
if delete_bucket:
    ! gsutil -m rm -r $BUCKET_URI
else:
    print(f"Bucket retained: {BUCKET_URI}")
```
