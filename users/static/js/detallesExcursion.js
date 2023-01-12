var modalWrap = null;
const showModal = (id, autor, exc) => {
        if (modalWrap !== null) {
            modalWrap.remove();
        }

        const csrftoken = token.innerHTML;

        modalWrap = document.createElement('div');
        modalWrap.innerHTML = `
        <div class="modal" tabindex="-1">
            <form method="post" action="responder_comentario/${exc}">
                <div class="modal-dialog">
                    ${csrftoken}
                    <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Responder a <span class="text-primary">${autor}</span> </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <input class="visually-hidden" name="comm" value="${id}">
                        <textarea class="form-control" rows="2" name="texto" required></textarea>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="submit" class="btn btn-primary">Comentar</button>
                    </div>
                    </div>
                </div>
            </form>
        </div>`;

        document.body.append(modalWrap);
        var modal = new bootstrap.Modal(modalWrap.querySelector('.modal'));
        modal.show();
    };
