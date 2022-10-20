// Global Helper Functions

function logMessage(msg) {
  if (store.cold.debugMode) {
    let caller = logMessage.caller;
    if (typeof caller === "function") {
      caller = caller.toString().substr("function ".length);
      caller = caller.substr(0, caller.indexOf("("));
    }
    const whatCalledWho = `${msg} triggered\n${caller}`;
    console.log(whatCalledWho);
    return whatCalledWho;
  }
}

// TODO: there is another unmerged branch with this util function (popup.js).
// Remove duplicate entry in popup.js after merge.
async function fetchGetJson(url) {
  try {
    // Default options are marked with *
    const response = await fetch(url, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
      mode: "cors", // no-cors, *cors, same-origin
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, *same-origin, omit
      headers: {
        "Content-Type": "application/json",
      }, redirect: "follow", // manual, *follow, error
      referrerPolicy: "no-referrer", // no-referrer, *client
    });
    return await response.json(); // parses JSON response into native JavaScript objects
  } catch (err) {
    if (err instanceof Error) {
      throw new Error(err.message);
    }
    throw err;
  }
}
