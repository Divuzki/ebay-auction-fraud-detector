(() => {
  let currentItemId = "";

  const loaderComponent = () => {
    return `<img style="width: 30px;" src="${chrome.runtime.getURL(
      "assets/spinner.gif"
    )}" />`;
  };

  const sendRequest = async () => {
    const response = await fetch(
      `http://localhost:8000/api/item/${currentItemId}`
    );
    const data = await response.json();

    return data;
  };

  const loadDivContainer = async () => {
    const ContainerExists = document.getElementsByClassName(
      "fraud-detector-container"
    )[0];

    if (!ContainerExists) {
      const divContainer = document.createElement("div");

      divContainer.innerHTML = `
      <div style="color: #fff;display: flex;user-select:none;align-items: center;">
        ${loaderComponent()}
        <span>Scanning Page For Fraud</span>
      </div>`;
      divContainer.style = `
      font: 12px/1.5 "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Geneva, Verdana, sans-serif;
      position: fixed;
      top: 7.5rem;
      right: 1rem;
      padding: 8px;
      background-color: rgb(68, 63, 63);
      border: 1px solid rgb(204, 204, 204);
      border-radius: 12px;`;

      document.body.appendChild(divContainer);
      // bookmarkBtn.addEventListener("click", addNewBookmarkEventHandler);
    }
  };

  chrome.runtime.onMessage.addListener((obj, sender, response) => {
    const { type, itemId } = obj;

    if (type === "ADD_PAGE_ACTION") {
      currentItemId = itemId;
      loadDivContainer();
    }
  });
  loadDivContainer();
})();
