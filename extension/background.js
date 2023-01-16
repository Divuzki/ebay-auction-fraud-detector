chrome.tabs.onUpdated.addListener((tabId, tab) => {
  if (tab.url && tab.url.includes("ebay.com/itm")) {
    // get the item id from the url
    const pageUrl = tab.url;
    let itemId = pageUrl.split("/").pop();
    if (itemId.includes("?")) {
      itemId = itemId.split("?")[0];
    }


    chrome.tabs.sendMessage(tabId, {
      type: "ADD_PAGE_ACTION",
      itemId: itemId,
    });
  }
});
