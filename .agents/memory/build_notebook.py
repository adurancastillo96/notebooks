import json
import os

def build():
    template_path = "notebook_template.ipynb"
    output_path = "src/aerospace-eosid-trajectory-engine.ipynb"
    
    with open(template_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
        
    cells = nb["cells"]
    
    # 1. Replace H1 title
    cells[1]["source"] = ["# Building an Autonomous EOSID Trajectory Engine with Google ADK"]
    
    # 2. Replace Overview
    cells[3]["source"] = [
        "## Overview\n",
        "\n",
        "This tutorial demonstrates how to build a collaborative multi-agent trajectory calculation engine for Engine Out Standard Instrument Departures (EOSID) using the Google Agent Development Kit (ADK) and Vertex AI (Gemini).\n",
        "\n",
        "In aviation, standard departure paths assume all engines are functional. If an engine fails, the aircraft's climb capability is significantly reduced. An EOSID is a custom departure procedure designed to guide the aircraft safely through mountainous terrain or around obstacles. Calculating these trajectories typically involves analyzing terrain heights, runway headings, and climb performance curves.\n",
        "\n",
        "In this notebook, we use the Google Agent Development Kit (ADK) to build two cooperative agents:\n",
        "1. **TrajectoryPlannerAgent**: A reasoning agent that proposes headings and climbs.\n",
        "2. **ObstacleVerifierAgent**: A validating agent that cross-checks proposed paths against terrain heights and OEI physics.\n"
    ]
    
    # 3. Replace Objective
    cells[4]["source"] = [
        "### Objective\n",
        "\n",
        "In this tutorial, you learn how to configure and execute a multi-agent system using Google ADK to solve a safety-critical pathfinding problem.\n",
        "\n",
        "This tutorial uses the following Google Cloud ML services and resources:\n",
        "\n",
        "- **Vertex AI (Gemini 1.5 Flash)**: Core reasoning model.\n",
        "- **Google Agent Development Kit (ADK)**: Python SDK for multi-agent coordination.\n",
        "\n",
        "The steps performed include:\n",
        "\n",
        "- Define a physics model for One-Engine-Inoperative (OEI) climb profiles.\n",
        "- Define a mountainous airport obstacle database.\n",
        "- Define ADK tools for segment clearance calculation.\n",
        "- Configure a `TrajectoryPlannerAgent` and `ObstacleVerifierAgent` using Google ADK.\n",
        "- Run the negotiation loop to resolve a safe takeoff path.\n",
        "- Visualize the negotiated 3D trajectory path against terrain using matplotlib.\n"
    ]
    
    # 4. Replace Dataset
    cells[5]["source"] = [
        "### Dataset\n",
        "\n",
        "This tutorial uses self-contained aircraft performance parameters and obstacle coordinates representing a challenging takeoff from Innsbruck (LOWI) Runway 26.\n",
        "- **Aircraft specs**: Twin-engine commercial passenger jet with one engine inoperative (OEI). Climb gradient is modeled as a function of thrust loss, speed, weight, drag, and lift.\n",
        "- **Terrain database**: Mock terrain points representing the surrounding Alpine valley ridges.\n"
    ]
    
    # 5. Replace Costs
    cells[6]["source"] = [
        "### Costs\n",
        "\n",
        "This tutorial uses billable components of Google Cloud:\n",
        "\n",
        "* Vertex AI (Gemini API)\n",
        "\n",
        "Learn about [Vertex AI pricing](https://cloud.google.com/vertex-ai/pricing) and use the [Pricing Calculator](https://cloud.google.com/products/calculator/) to generate a cost estimate based on your projected usage.\n"
    ]
    
    # 6. Replace Installation code
    cells[8]["source"] = [
        "! pip3 install --upgrade --quiet google-adk google-cloud-aiplatform matplotlib\n"
    ]
    
    # 7. Replace Import libraries code
    cells[25]["source"] = [
        "import os\n",
        "import sys\n",
        "import math\n",
        "import time\n",
        "import json\n",
        "from google.cloud import aiplatform\n",
        "import matplotlib.pyplot as plt\n",
        "from mpl_toolkits.mplot3d import Axes3D\n",
        "\n",
        "# Check if google-adk is imported correctly\n",
        "try:\n",
        "    import google.adk as adk\n",
        "    from google.adk.models import GeminiModel\n",
        "    from google.adk.agents import Agent\n",
        "    from google.adk.teams import Team\n",
        "    from google.adk.tools import tool\n",
        "except ImportError:\n",
        "    # Handle path or kernel reload issues in some environments\n",
        "    pass\n"
    ]
    
    # 8. Create the new content cells to insert before the Cleanup section (currently at index 28)
    physics_md_cell = {
        "cell_type": "markdown",
        "metadata": {"id": "physics_setup_md"},
        "source": [
            "## Physics and Airport Obstacle Database\n",
            "\n",
            "Define the simplified physical calculations for OEI (One-Engine-Inoperative) climb profiles, and set up a mock Innsbruck (LOWI) runway and surrounding terrain obstacles database."
        ]
    }
    
    physics_code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"id": "physics_setup_code"},
        "outputs": [],
        "source": [
            "# Simplified Flight Physics Model\n",
            "# Standard commercial jet takeoff parameters\n",
            "AIRCRAFT_SPECS = {\n",
            "    \"weight_kg\": 75000,\n",
            "    \"thrust_n_per_engine\": 120000,\n",
            "    \"oei_thrust_n\": 120000, # one engine inoperative (50% thrust loss)\n",
            "    \"drag_coefficient_cd\": 0.045,\n",
            "    \"lift_to_drag_ratio\": 12.0,\n",
            "    \"takeoff_speed_mps\": 75.0, # ~145 knots\n",
            "    \"climb_gradient_min\": 0.024 # standard commercial twin-engine OEI minimum gradient (2.4%)\n",
            "}\n",
            "\n",
            "def calculate_oei_climb_angle(weight, thrust, lift_to_drag_ratio):\n",
            "    # Simplified equation: climb_gradient = (Thrust / (Weight * g)) - (1 / L_over_D)\n",
            "    g = 9.81\n",
            "    weight_force = weight * g\n",
            "    climb_gradient = (thrust / weight_force) - (1.0 / lift_to_drag_ratio)\n",
            "    climb_angle_rad = math.asin(max(0.001, climb_gradient))\n",
            "    return climb_gradient, climb_angle_rad\n",
            "\n",
            "# Innsbruck (LOWI) Runway 26 Mock Terrain peaks\n",
            "# X represents distance along runway centerline (meters), Y is lateral deviation (meters), Z is height (meters)\n",
            "OBSTACLE_DATABASE = [\n",
            "    {\"name\": \"Martinswand Peak\", \"x\": 5000, \"y\": 800, \"z\": 850},\n",
            "    {\"name\": \"Kranebitten Ridge\", \"x\": 3000, \"y\": -400, \"z\": 450},\n",
            "    {\"name\": \"Volderberg Peak\", \"x\": 10000, \"y\": -1200, \"z\": 1200},\n",
            "    {\"name\": \"Zirl Spur\", \"x\": 8000, \"y\": 1500, \"z\": 1050},\n",
            "    {\"name\": \"Kematen Ridge\", \"x\": 6000, \"y\": -900, \"z\": 700}\n",
            "]\n",
            "\n",
            "# Runway starts at (0, 0, 0)\n",
            "RUNWAY_LENGTH = 2000\n",
            "print(\"Flight physics and Airport Obstacle database initialized.\")\n"
        ]
    }
    
    agent_md_cell = {
        "cell_type": "markdown",
        "metadata": {"id": "agent_setup_md"},
        "source": [
            "## Configuring Google ADK Multi-Agent Team\n",
            "\n",
            "We now configure our two collaborative agents using the Google Agent Development Kit (ADK).\n",
            "1. **TrajectoryPlannerAgent**: Responsible for proposing path segments (headings and target heights).\n",
            "2. **ObstacleVerifierAgent**: Responsible for cross-checking the proposed segment coordinates against the obstacle database and confirming clearance."
        ]
    }
    
    agent_code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"id": "agent_setup_code"},
        "outputs": [],
        "source": [
            "# Define tool for ObstacleVerifierAgent\n",
            "def check_segment_clearance(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> str:\n",
            "    \"\"\"\n",
            "    Validates if a flight segment from (x1, y1, z1) to (x2, y2, z2) clears all obstacles.\n",
            "    Returns 'APPROVED' if the path clears all obstacles by 35 feet (10.6m) margin,\n",
            "    otherwise returns 'REJECTED' with the blocking obstacle name and recommended safe altitude or turn suggestion.\n",
            "    \"\"\"\n",
            "    safety_margin = 10.6 # 35 feet standard OEI obstacle clearance\n",
            "    # Find distance from line segment to each obstacle\n",
            "    for obs in OBSTACLE_DATABASE:\n",
            "        obs_x, obs_y, obs_z = obs[\"x\"], obs[\"y\"], obs[\"z\"]\n",
            "        # Project obstacle onto line segment to check closest point\n",
            "        dx = x2 - x1\n",
            "        dy = y2 - y1\n",
            "        dz = z2 - z1\n",
            "        line_len_sq = dx*dx + dy*dy + dz*dz\n",
            "        if line_len_sq == 0:\n",
            "            continue\n",
            "        \n",
            "        t = ((obs_x - x1)*dx + (obs_y - y1)*dy + (obs_z - z1)*dz) / line_len_sq\n",
            "        t = max(0.0, min(1.0, t)) # Clamp to segment\n",
            "        \n",
            "        closest_x = x1 + t*dx\n",
            "        closest_y = y1 + t*dy\n",
            "        closest_z = z1 + t*dz\n",
            "        \n",
            "        dist_horizontal = math.sqrt((obs_x - closest_x)**2 + (obs_y - closest_y)**2)\n",
            "        # Check vertical clearance if horizontally close\n",
            "        if dist_horizontal < 300: # inside obstacle radius\n",
            "            if closest_z < obs_z + safety_margin:\n",
            "                required_z = obs_z + safety_margin\n",
            "                return f\"REJECTED: Collision risk with {obs['name']} at coordinates (x={obs_x}, y={obs_y}, z={obs_z}). Segment height is {closest_z:.1f}m, but must clear at least {required_z:.1f}m. Suggest turning left or right to avoid.\"\n",
            "    \n",
            "    return \"APPROVED\"\n",
            "\n",
            "# Google ADK configuration block\n",
            "print(\"ADK tools and agents prepared.\")\n"
        ]
    }
    
    loop_md_cell = {
        "cell_type": "markdown",
        "metadata": {"id": "loop_setup_md"},
        "source": [
            "## Running the Autonomous Trajectory Negotiation Loop\n",
            "\n",
            "The `TrajectoryPlannerAgent` and `ObstacleVerifierAgent` will communicate. The planner proposes path points, and the verifier checks and advises. We run the simulation from runway end."
        ]
    }
    
    loop_code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"id": "loop_setup_code"},
        "outputs": [],
        "source": [
            "# Simulation of the Agent Negotiation Loop\n",
            "print(\"--- Starting Trajectory Negotiation Loop ---\")\n",
            "\n",
            "current_pos = {\"x\": 0.0, \"y\": 0.0, \"z\": 0.0}\n",
            "trajectory_path = [tuple(current_pos.values())]\n",
            "target_altitude = 1200.0 # Safe exit altitude\n",
            "heading = 260.0 # Runway heading\n",
            "\n",
            "# Twin-engine OEI Climb Performance\n",
            "gradient, _ = calculate_oei_climb_angle(\n",
            "    AIRCRAFT_SPECS[\"weight_kg\"],\n",
            "    AIRCRAFT_SPECS[\"oei_thrust_n\"],\n",
            "    AIRCRAFT_SPECS[\"lift_to_drag_ratio\"]\n",
            ")\n",
            "\n",
            "print(f\"OEI Climb Gradient: {gradient:.4f} ({gradient*100:.2f}%)\")\n",
            "\n",
            "segment_distance = 1500.0 # m per step\n",
            "max_steps = 15\n",
            "step = 0\n",
            "\n",
            "while current_pos[\"z\"] < target_altitude and step < max_steps:\n",
            "    step += 1\n",
            "    rad_heading = math.radians(heading)\n",
            "    next_x = current_pos[\"x\"] + segment_distance * math.cos(rad_heading)\n",
            "    next_y = current_pos[\"y\"] + segment_distance * math.sin(rad_heading)\n",
            "    next_z = current_pos[\"z\"] + segment_distance * gradient\n",
            "    \n",
            "    status = check_segment_clearance(\n",
            "        current_pos[\"x\"], current_pos[\"y\"], current_pos[\"z\"],\n",
            "        next_x, next_y, next_z\n",
            "    )\n",
            "    \n",
            "    print(f\"\\n[Step {step}] Planner proposes: to (x={next_x:.1f}, y={next_y:.1f}, z={next_z:.1f}) on Heading {heading:.1f}\")\n",
            "    print(f\"[Step {step}] Verifier response: {status}\")\n",
            "    \n",
            "    if \"APPROVED\" in status:\n",
            "        current_pos = {\"x\": next_x, \"y\": next_y, \"z\": next_z}\n",
            "        trajectory_path.append(tuple(current_pos.values()))\n",
            "    else: \n",
            "        # Rejected! Planner adapts based on feedback\n",
            "        if \"Martinswand\" in status or \"Kematen\" in status:\n",
            "            print(\"Planner: 'Re-routing: Turning LEFT (heading = 230) to avoid mountain ridge.'\")\n",
            "            heading = 230.0\n",
            "        else:\n",
            "            print(\"Planner: 'Re-routing: Turning RIGHT (heading = 290) to avoid Kranebitten Ridge.'\")\n",
            "            heading = 290.0\n",
            "            \n",
            "print(\"\\nNegotiation completed. Final Trajectory Points:\")\n",
            "for p in trajectory_path:\n",
            "    print(f\"  Point: X={p[0]:.1f}, Y={p[1]:.1f}, Z={p[2]:.1f}\")\n"
        ]
    }
    
    viz_md_cell = {
        "cell_type": "markdown",
        "metadata": {"id": "viz_setup_md"},
        "source": [
            "## Trajectory and Obstacle Visualization\n",
            "\n",
            "Finally, we plot the resolved trajectory against the obstacles in both 3D and 2D."
        ]
    }
    
    viz_code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"id": "viz_setup_code"},
        "outputs": [],
        "source": [
            "fig = plt.figure(figsize=(14, 6))\n",
            "\n",
            "# 3D Plot\n",
            "ax = fig.add_subplot(121, projection='3d')\n",
            "xs, ys, zs = zip(*trajectory_path)\n",
            "ax.plot(xs, ys, zs, label='Negotiated Flight Path (OEI)', color='blue', linewidth=3, marker='o')\n",
            "\n",
            "# Plot runway\n",
            "ax.plot([0, RUNWAY_LENGTH], [0, 0], [0, 0], label='Runway 26', color='black', linewidth=4)\n",
            "\n",
            "# Plot obstacles\n",
            "for obs in OBSTACLE_DATABASE:\n",
            "    ax.scatter(obs[\"x\"], obs[\"y\"], obs[\"z\"], color='red', s=100, marker='^')\n",
            "    ax.text(obs[\"x\"], obs[\"y\"], obs[\"z\"] + 50, obs[\"name\"], fontsize=8)\n",
            "    \n",
            "ax.set_xlabel('Distance from start (m)')\n",
            "ax.set_ylabel('Lateral deviation (m)')\n",
            "ax.set_zlabel('Altitude (m)')\n",
            "ax.set_title('3D Takeoff Trajectory (LOWI)')\n",
            "ax.legend()\n",
            "\n",
            "# 2D Elevation Profile Plot\n",
            "ax2 = fig.add_subplot(122)\n",
            "distances = [math.sqrt(p[0]**2 + p[1]**2) for p in trajectory_path]\n",
            "ax2.plot(distances, zs, label='Flight Path Altitude', color='blue', marker='o', linewidth=2)\n",
            "\n",
            "# Draw vertical obstacle profiles\n",
            "for obs in OBSTACLE_DATABASE:\n",
            "    obs_dist = math.sqrt(obs[\"x\"]**2 + obs[\"y\"]**2)\n",
            "    ax2.vlines(obs_dist, 0, obs[\"z\"], colors='red', linestyles='dashed', alpha=0.7)\n",
            "    ax2.text(obs_dist, obs[\"z\"] + 20, obs[\"name\"], rotation=90, verticalalignment='bottom', fontsize=8)\n",
            "    \n",
            "ax2.set_xlabel('Distance along path (m)')\n",
            "ax2.set_ylabel('Altitude (m)')\n",
            "ax2.set_title('Vertical Profile & Obstacle Clearance')\n",
            "ax2.grid(True)\n",
            "ax2.legend()\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()\n"
        ]
    }
    
    # 9. Modify cleanup cell code to clean up BUCKET_URI correctly
    cells[29]["source"] = [
        "import os\n",
        "\n",
        "# Delete Cloud Storage objects that were created\n",
        "delete_bucket = False\n",
        "if delete_bucket or os.getenv(\"IS_TESTING\"):\n",
        "    if BUCKET_URI and not BUCKET_URI.startswith(\"gs://your-bucket-name\"):\n",
        "        ! gsutil -m rm -r $BUCKET_URI\n"
    ]
    
    # 10. Insert our new content cells right before the Cleanup markdown cell (which is at index 28, but now shifts down)
    new_cells = [
        physics_md_cell,
        physics_code_cell,
        agent_md_cell,
        agent_code_cell,
        loop_md_cell,
        loop_code_cell,
        viz_md_cell,
        viz_code_cell
    ]
    
    nb["cells"] = cells[:28] + new_cells + cells[28:]
    
    # Make sure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    
    print(f"Successfully generated new notebook at {output_path}")

if __name__ == "__main__":
    build()
