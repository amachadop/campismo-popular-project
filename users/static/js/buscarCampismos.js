const buscarCampismos = async (keywords, provincia, val, min, max, categoria, turismo) => {
    try {
        const response = await fetch(`buscar/lista/${keywords}/${provincia}/${val}/${min}/${max}/${categoria}/${turismo}/`);
        const data = await response.json();

        if (data.message == "success") {
            actualizarCampismos(data.campismos, data.provincias);
        } else {
            noCampismosEncontrados();
        }

    } catch (e) {
        console.log(e);
    }
};

const cargaInicial = async () => {
    await buscarCampismos("*all", selectProvincia.value, valoracionSearch.value, 0, 10000, selectCategoria.selectedIndex, "C");

    btn_buscar.addEventListener("click", () => {
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

        var tipoT = "A";
        switch (selectTurismo.value) {
            case "Cualquiera":
                tipoT = "C";
                break;
            case "Ambos":
                tipoT = "A";
                break;

            case "Nacional":
                tipoT = "N";
                break;

            case "Internacional":
                tipoT = "I";
                break;
        }

        buscarCampismos(str, selectProvincia.value, valoracionSearch.value, min, max, selectCategoria.selectedIndex, tipoT);
    });

    btnRefresh.addEventListener("click", () => {
        keywordsSerch.value = "";
        selectProvincia.selectedIndex = 0;
        valoracionSearch.value = 0;
        precioMin.value = "";
        precioMax.value = "";
        selectCategoria.selectedIndex = 0;
        selectTurismo.selectedIndex = 0;
    });

};

window.addEventListener("load", async () => {
    await cargaInicial();
});


function actualizarCampismos(campismos, provincias) {
    // ` with alt+96

    let visual = ``;

    campismos.forEach((camp) => {

        visual += `<div class="col">
                        <a href="${camp.id}">
                            <div class="mycard shadow">
                                <div class="poster"><img src="http://${window.location.hostname}:${window.location.port}/media/${camp.foto}"> </div>
                                    <div class="details-campismo">
                                        <h4 class="mb-3 fw-semibold text-light">${camp.nombre}</h4>
                                        ${setRate(camp.rate)}
                                        <div class="mb-2 mt-3">
                                                <h6 class="card-subtitle mb-2 text-light">${getNombreProvincia(camp.provincia_id, provincias)}</h6>
                                        </div>
                                        <div class="d-flex mt-2 mb-2">
                                            <h6 class="card-subtitle mb-2 text-light float-end">Precio Temporada Alta: $${camp.precioTA} x 🧍</h6>
                                            <h6 class="card-subtitle mb-2 text-light float-end">Precio Temporada Baja: $${camp.precioTB} x 🧍</h6>
                                        </div>
                                        <div class="d-flex mt-2 mb-2">
                                            <img src="${imgSRC.src}categoria${camp.categoria}.svg" style="width: 25px" class="me-2">
                                            ${getImgTurismo(camp.tipoTurismo)}
                                        </div>
                                </div>
                            </div>
                        </a>
                    </div>`;
    });

    campContainer.innerHTML = visual;

}

function noCampismosEncontrados() {
    campContainer.innerHTML = `<h6 class="text-success fw-semibold mb-3 text-center"> No se encontraron coincidencias </h6>`;
}

getImgTurismo = (t) => {
    switch (t) {
        case "N":
            return `<img src="${imgSRC.src}nacional.svg" style="width: 25px">`;

        case "I":
            return `<img src="${imgSRC.src}internacional.svg" style="width: 25px">`;

        case "NI":
            return `<img src="${imgSRC.src}nacional.svg" style="width: 25px" class="me-1">` + `<img src="${imgSRC.src}internacional.svg" style="width: 25px">`;
    }
};

function getNombreProvincia(id, provincias) {
    var n = "";
    provincias.forEach((p) => {
        if (p.id == id) {
            n = p.nombre;
        }
    });
    return n;
}

function setRate(rate) {
    console.log(rate);
    let visual = ``;

    if (rate==null){
        visual = `<p class="text-warning">No tiene valoraciones</p>`;
    }else{
        var i = 1;
        while (i <= 5) {
            if (i > rate) {
                visual += `<span class="material-symbols-outlined text-warning">star_rate</span>`;
            } else {
                visual += `<span class="material-symbols-rounded text-warning">grade</span>`;
            }
            i++;
        }
    }

    return visual;
}

