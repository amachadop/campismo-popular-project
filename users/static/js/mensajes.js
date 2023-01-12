var modalWrap = null;
const successMessage = (message) => {
    if (modalWrap !== null) {
        modalWrap.remove();
    }
    modalWrap = document.createElement('div');
    modalWrap.innerHTML = `
        <div class="modal fade" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header border-0">
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body text-center">
                        <h4 class="fw-light text-success">${message}</h4>
                    </div>
                    <div class="modal-footer border-0">
                        <button type="button" class="btn btn-success" data-bs-dismiss="modal">Aceptar</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.body.append(modalWrap);

    var modal = new bootstrap.Modal(modalWrap.querySelector('.modal'));
    modal.show();
};

const errorMessage = (message) => {
    if (modalWrap !== null) {
        modalWrap.remove();
    }
    modalWrap = document.createElement('div');
    modalWrap.innerHTML = `
        <div class="modal fade" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header border-0">
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body text-center">
                        <h4 class="fw-light text-danger">${message}</h4>
                    </div>
                    <div class="modal-footer border-0">
                        <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Aceptar</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.body.append(modalWrap);

    var modal = new bootstrap.Modal(modalWrap.querySelector('.modal'));
    modal.show();
};