window.addEventListener("load", async () => {
    await buscarExcursiones("*all", "True", 0, 10000);

    btn_buscar.addEventListener("click", async () => {
        var str = keywordsSerch.value;
        if (str == "") {
            str = "*all";
        }
        var min = precioMin.value;
        var max = precioMax.value;

        if (min == "") {
            min = 0;
        }

        if (max == "") {
            max = 10000;
        }

        var d = checkDisponible.checked;
        if (d == true) {
            d = "True";
        } else {
            d = "False";
        }

        await buscarExcursiones(str, d, min, max);

    });

    btnRefresh.addEventListener("click", () => {

        keywordsSerch.value = "";
        precioMin.value = 0;
        precioMax.value = 10000;
        checkDisponible.checked = false;

    });

});

const buscarExcursiones = async (keywords, disponible, precioMin, precioMax) => {
    try {

        const response = await fetch(`lista/${keywords}/${disponible}/${precioMin}/${precioMax}/`);
        const data = await response.json();

        if (data.message == "success") {
            actualizarExcursiones(data.excursiones)
        } else {
            excContainer.innerHTML = `<h6 class="text-success fw-semibold mb-3 text-center"> No se encontraron coincidencias </h6>`;
        }

    } catch (e) {
        console.log(e);
    }
};

function actualizarExcursiones(excursiones) {

    let visual = ``;

    excursiones.forEach((e) => {

        visual += `<div class="col" >
        <a href="${e.id}">
        <div class="mycard shadow">
        <div class="poster">
        <img src="http://${window.location.hostname}:${window.location.port}/media/${e.foto}">
                   </div>
                   <div class="details">
                   <h4 class="mb-3 fw-semibold text-light">${e.nombre}</h4>
                                                                                            <div class="row mb-2">
                                                                                            <div class="col-sm">
                                                                                            <h6 class="card-subtitle mb-2 text-light">${e.destino}</h6>
                                                                      </div>
                                                                      <div class="col-sm">
                                                                      <h6 class="card-subtitle mb-2 text-light float-end">$${e.precio} x 🧍</h6>
                                                                                                                                                  </div>
                                                                                                                                                  </div>
                                                                                                                                                  </div>
                                                                                                                                                  </div>
                    </a>
            </div>`;

    });

    excContainer.innerHTML = visual;

};