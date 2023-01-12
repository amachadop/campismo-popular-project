window.addEventListener("load", async () => {
    await cargaIncial();

    if (error.innerHTML != ""){
        errorMessage(error.innerHTML);
    }

});

const cargaIncial = async () => {
    await getFechasCanceladas();
};

const getFechasCanceladas = async () => {
    try {
        const response = await fetch(`./getFechasCancel`);
        const data = await response.json();

        if (data.message == "success") {
            flatpickr(fechaReservas, {
                mode: "range",
                minDate: "today",
                disable: data.fechas_cancel
            });
        } else {
            flatpickr(fechaReservas, {
                mode: "range",
                minDate: "today"
            });
        }

    } catch (e) {
        console.log(e);
    }
};


