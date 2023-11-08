window.onload = function() {
  const button = document.getElementById("button");

  button.onclick = function() {
    let problemName;
    chrome.tabs.query(
      {active: true},
      async (tabs) => {
        const tab = tabs[0];
        let urlParams = tab.url.split("problems")[1];
        if (urlParams === undefined) {
          document.getElementById("textarea").value = "Invalid leetcode problem or link, try again";
          return
        }
        urlParams = urlParams.slice(1);
        const endSlash = urlParams.indexOf("/");
        if (urlParams === undefined || endSlash === -1) {
          document.getElementById("textarea").value = "Invalid leetcode problem or link, try again";
          return;
        }
        problemName = urlParams.slice(0, endSlash);
        const solution = await fetchSolution(problemName);
        document.getElementById("textarea").value = solution;
      }
    )
  }
}

const fetchSolution = async (problemName) => {
  let solution = await fetch(`http://127.0.0.1:5000/problem/${problemName}`);
  try {
    ans = await solution.json();
  } catch (err) {
    return "Not a neetcode problem, try again on a different problem!"
  }
  return ans;
}
