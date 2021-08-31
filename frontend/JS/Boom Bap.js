function renderproducts(beats) {
    let beatContainer = document.querySelector("#container");
    beatContainer.innerHTML = "";
    beats.forEach((beats) => {
      beatContainer.innerHTML += `
      <div class="beat-box">
      <div class="beats" catergory=${beats[2]}>
      <h3 class="image items"><img src="${beats[4]}"></h3>
      <div class="info">
      <h3 class="beat_name items">${beats[1]}</h3>
      <h3 class="beat_type items">${beats[2]}</h3>
      <h3 class="beat_tempo items">${beats[3]}</h3>
      <h3 class="producer items">${beats[5]}</h3>
      <h3 class="price items">R${beats[6]}</h3>
      </div>
      </div>
      </div>
      `;
    });
}
  
  
  function filterTrap(catergory) {
      fetch("https://fast-bayou-16865.herokuapp.com/display-beats/")
      .then((response) => response.json())
      .then((json) => {
          beats = json.data
          let filterBeats = beats.filter((beat) => {
             return beat[2].toLowerCase() == catergory.toLowerCase()
          })
          renderproducts(filterBeats)
      });
  }
  
  filterTrap("boom bap")
