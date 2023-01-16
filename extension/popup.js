import { getActiveTabURL } from "./utils.js";

document.addEventListener("DOMContentLoaded", async () => {
  const activeTab = await getActiveTabURL();
  // get the item id from the url
  const pageUrl = activeTab.url;
  let itemId = pageUrl.split("/").pop();
  if (itemId.includes("?")) {
    itemId = itemId.split("?")[0];
  }

  if (activeTab.url.includes("ebay.com/itm") && itemId) {
    const container = document.getElementsByClassName("container")[0];

    container.innerHTML = '<div class="title">This is an ebay item page.</div>';
  } else {
    const container = document.getElementsByClassName("container")[0];

    container.innerHTML =
      '<div class="title">This is not an ebay item page.</div>';
  }
});
