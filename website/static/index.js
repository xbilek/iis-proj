function deleteTeam(team_name) {
    fetch("/delete-team", {
      method: "POST",
      body: JSON.stringify({ team_name: team_name }),
    }).then((_res) => {
      window.location.href = "/test";
    });
  }
