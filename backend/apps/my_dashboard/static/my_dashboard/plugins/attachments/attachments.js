$(document).ready(function () {
    const FILE_TYPES_ICONS = {
        "word": "fa fa-file-word fa-3x",
        "pdf": "fa fa-file-pdf fa-3x",
        "text": "fa fa-file-text fa-3x",
        "image": "fa fa-file-image fa-3x",
        "video": "fa fa-file-video fa-3x",
        "file": "fa fa-file fa-3x",
    }
    const FILE_TYPES_EXTENSIONS = {
        "word": [".doc", ".docx", ".word",],
        "pdf": [".pdf",],
        "text": [".text", ".txt",],
        "image": ['.jpg', '.jpeg', '.png',],
        "video": ['.mp4', '.avi',],
    }

    function formatFileSize(sizeInBytes) {
        if (sizeInBytes === undefined || sizeInBytes === null) {
            return "";
        }
        const units = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        if (sizeInBytes === 0) return '0 Bytes';
        const unitIndex = Math.floor(Math.log(sizeInBytes) / Math.log(1024));
        const readableSize = (sizeInBytes / Math.pow(1024, unitIndex)).toFixed(2);
        return `${readableSize} ${units[unitIndex]}`;
    }

    const attachmentsState = {
        attachmentsList: {
            data: [],
            isLoading: false,
        },
        modal: {
            useSelectAttachment: false,
            currentInputWidgetBaseId: null,
            open: false,
            currentAttachmentSelection: null,
            currentAttachmentValue: null,
        },
        delete: {
            isLoading: false,
        },
        upload: {
            isLoading: false,
            currentAttachmentFileValue: null,
        }
    };

    class ThumbnailAttachmentWidget {
        constructor() {
        }

        setInitialElements(container_el) {
            this.container_el = container_el;
            this.input_el = this.container_el.find(".thumbnail-attachment-field");
            this.upload_btn_el = this.container_el.find(".thumbnail-upload-btn");
            this.remove_btn_el = this.container_el.find(".thumbnail-remove-btn");
            this.attachment_btn_el = this.container_el.find(".thumbnail-from-attachments-btn");
            this.thumbnail_img_preview_container_el = this.container_el.find(`.thumbnail-image-preview-container`);
            this.thumbnail_img_preview_el = this.thumbnail_img_preview_container_el.find(`.thumbnail-image-preview-img`);
            this.widget_id_base = this.input_el.data("widget-id-base");

            this.formState = {
                uploadAttachmentFile: null,
                currentValue: null,
            }
        }

        initFormState() {
            this.upload_btn_el.attr("disabled", true);
            const data = this.input_el.data();
            this.setInputValue(data);
        }

        setInputValue(value = {}) {
            const updated = {
                id: value.id || "",
                name: value.name || "",
                url: value.url || "",
                alt: value.alt || "",
            }
            const input_el = this.input_el;
            const new_input_value = updated.id;
            input_el.val(new_input_value);
            Object.keys(updated).forEach(function (key) {
                input_el.attr(`data-${key}`, updated[key]);
            });
            this.thumbnail_img_preview_el.attr("src", updated.url);
            this.thumbnail_img_preview_el.attr("alt", updated.alt);
            this.remove_btn_el.attr("disabled", !updated.id);
            if (updated.url) {
                this.thumbnail_img_preview_el.addClass("active");
            } else {
                this.thumbnail_img_preview_el.removeClass("active");
            }
            this.formState.currentValue = new_input_value;
        }
    }

    function fetchActionRelatedObject(config, callbacks = {
        success: null,
    }) {
        const formData = new FormData();
        formData.append('content_type', attachmentsData.content_type);
        formData.append('object_id', attachmentsData.object_id);
        formData.append('attachment_type', config.attachment_type);
        formData.append('to_model_field_name', config.to_model_field_name);
        formData.append('action', config.action);
        formData.append('obj_id', config.obj_id);
        $.ajax({
            url: attachmentsData.action.apiUrl,
            type: 'POST',
            data: formData,
            dataType: 'JSON',
            mimeType: "multipart/form-data",
            contentType: false,
            cache: false,
            processData: false,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", $("[name=csrfmiddlewaretoken]").attr("value"));
            },
            error: function () {
            },
            success: function (response) {
                if (callbacks.success) {
                    callbacks.success(response);
                }
            }
        });
    }

    function fetchSaveRelatedObjectThumbnail(item, callbacks = {
        success: null,
    }) {
        const formData = new FormData();
        formData.append('content_type', attachmentsData.content_type);
        formData.append('object_id', attachmentsData.object_id);
        formData.append('attachment_type', "thumbnail_image");
        formData.append('file', item.formState.uploadAttachmentFile);
        formData.append('to_model_field_name', "thumbnail");
        $.ajax({
            url: attachmentsData.upload.apiUrl,
            type: 'POST',
            data: formData,
            dataType: 'JSON',
            mimeType: "multipart/form-data",
            contentType: false,
            cache: false,
            processData: false,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", $("[name=csrfmiddlewaretoken]").attr("value"));
            },
            error: function () {
            },
            success: function (response) {
                if (!response.url) {
                    response.url = response.file;
                }
                item.setInputValue(response);
                item.formState.uploadAttachmentFile = null;
                item.thumbnail_img_preview_el.addClass("active");
                item.upload_btn_el.attr("disabled", true);
                if (callbacks.success) {
                    callbacks.success(response);
                }
            }
        });
    }

    const thumbnailAttachmentWidgetsList = [];
    $(".thumbnail-attachment-container").each(function (index) {
        const item = new ThumbnailAttachmentWidget();
        item.setInitialElements($(this));
        item.initFormState();
        thumbnailAttachmentWidgetsList.push(item);

        const initialDisabled = item.input_el.data("initial-disabled");
        if(!!initialDisabled) {
            item.upload_btn_el.attr("disabled", true);
            item.remove_btn_el.attr("disabled", true);
            item.attachment_btn_el.attr("disabled", true);
            item.container_el.addClass("initial-disabled");
        }
    });
    const attachments_list_modal_el = $("#attachments-list-modal");
    const attachments_list_grid_el = attachments_list_modal_el.find(".attachments-list-grid");
    const selection_confirm_btn_el = attachments_list_modal_el.find(".selection-confirm-btn");

    function loadAttachments(filters = {}, callbacks = {
        success: null,
    }) {
        const filtersData = Object.assign({
            content_type: attachmentsData.content_type,
            object_id: attachmentsData.object_id,
        }, {});
        attachmentsState.attachmentsList.isLoading = true;
        $.ajax({
            url: attachmentsData.listApiUrl,
            method: "GET",
            data: filtersData,
            dataType: "json",
            success: function (response) {
                const response_results = response.results;
                let html = "";
                response_results.forEach(function (el) {
                    let selectedExtensionIconKey = "file";
                    Object.keys(FILE_TYPES_EXTENSIONS).forEach(function (key) {
                        if (FILE_TYPES_EXTENSIONS[key].includes(el.extension)) {
                            selectedExtensionIconKey = key;
                        }
                    });
                    const icon_class = FILE_TYPES_ICONS[selectedExtensionIconKey];
                    let icon_html = (`<i class="${icon_class}"></i>`);
                    if (selectedExtensionIconKey === "image") {
                        icon_html = `<img src="${el.file}" alt="${el.alt}" />`
                    }
                    html += (
                        `<div class="col-lg-3 col-xl-2">
                            <div class="file-man-box" data-item-id="${el.id}">
                                <a href="" class="file-close"><i class="fa fa-times-circle"></i></a>
                                <div class="file-img-box">${icon_html}</div>
                                <a href="${el.file}" class="file-download">
                                    <i class="fa fa-download"></i>
                                </a>
                                <div class="file-man-title">
                                    <h5 class="mb-0 text-overflow">${el.name}</h5>
                                    <p class="mb-0"><small>${formatFileSize(el.size)}</small></p>
                                </div>
                            </div>
                        </div>`
                    );
                });
                attachments_list_grid_el.html(html);
                attachmentsState.attachmentsList.data = response_results;
                if (callbacks && callbacks.success) {
                    callbacks.success(response, response_results);
                }
            },
            always: function () {
                attachmentsState.attachmentsList.isLoading = false;
                // console.log("always"); // todo: fix always
            }
        });
    }

    function openAttachmentsModal(config = {}) {
        attachmentsState.modal.open = true;
        attachmentsState.modal.currentInputWidgetBaseId = null;
        attachmentsState.modal.useSelectAttachment = false;
        attachmentsState.modal.currentAttachmentSelection = null;
        attachmentsState.modal = Object.assign(attachmentsState.modal, config);
        if (attachmentsState.modal.useSelectAttachment) {
            attachments_list_grid_el.addClass("use-selection");
            selection_confirm_btn_el.attr("disabled", true);
        } else {
            attachments_list_grid_el.removeClass("use-selection");
            selection_confirm_btn_el.attr("disabled", false);
        }
        attachments_list_modal_el.modal("show");
    }

    function closeAttachmentsModal(config = {}) {
        attachmentsState.modal.open = false;
        attachmentsState.modal.currentInputWidgetBaseId = null;
        attachmentsState.modal.useSelectAttachment = false;
        attachmentsState.modal.currentAttachmentSelection = null;
        attachmentsState.modal = Object.assign(attachmentsState.modal, config);
        attachments_list_modal_el.modal("hide");
    }

    $(`.thumbnail-from-attachments-btn`).on("click", function () {
        const inputField = $(this).closest('div').siblings('input.thumbnail-attachment-field');
        const baseId = inputField.data("widget-id-base");
        if (!baseId) {
            console.error("input's widget-id-base can not be empty");
            return;
        }
        openAttachmentsModal({
            useSelectAttachment: true,
            currentInputWidgetBaseId: baseId,
            currentAttachmentSelection: null,
        });
        loadAttachments({}, {
            success: function (response, data_list) {
                selectAttachmentCard(baseId);
            },
        });
    });
    selection_confirm_btn_el.on("click", function () {
        if (!attachmentsState.modal.currentAttachmentSelection) {
            console.error("currentAttachmentSelection not selected yet.");
            return;
        }
        const widget_item = thumbnailAttachmentWidgetsList.find(function (item) {
            return item.widget_id_base === attachmentsState.modal.currentInputWidgetBaseId;
        });
        fetchActionRelatedObject({
            attachment_type: "thumbnail_image",
            to_model_field_name: "thumbnail",
            action: "attach_related_single",
            obj_id: attachmentsState.modal.currentAttachmentSelection.id,
        }, {
            success: function (response) {
                const data = attachmentsState.modal.currentAttachmentSelection;
                if (!data.url) {
                    data.url = data.file;
                }
                widget_item.setInputValue(data);
                closeAttachmentsModal();
            }
        });
    });
    attachments_list_modal_el.on('hidden.bs.modal', function () {
        attachmentsState.modal = {
            useSelectAttachment: false,
            currentInputWidgetBaseId: null,
            open: false,
            currentAttachmentSelection: null,
        };
    });

    function selectAttachmentCard(selectId) {
        if (attachmentsState.modal.currentAttachmentSelection) {
            $(`.attachments-list .attachments-list-grid .file-man-box[data-item-id=${attachmentsState.modal.currentAttachmentSelection.id}]`).removeClass("selected");
        }
        const card_el = $(`.attachments-list .attachments-list-grid .file-man-box[data-item-id=${selectId}]`);
        if (attachmentsState.modal.currentAttachmentSelection) {
            if (attachmentsState.modal.currentAttachmentSelection.id === selectId) {
                selection_confirm_btn_el.attr("disabled", true);
                attachmentsState.modal.currentAttachmentSelection = null;
                return;
            }
        }
        card_el.addClass("selected");
        attachmentsState.modal.currentAttachmentSelection = attachmentsState.attachmentsList.data.find(function (item) {
            return item.id === selectId;
        });
        if (attachmentsState.modal.currentAttachmentSelection) {
            selection_confirm_btn_el.attr("disabled", false);
        } else {
            selection_confirm_btn_el.attr("disabled", true);
        }
    }

    $(document).on("click", `.file-man-box`, function () {
        if (attachmentsState.modal.open && attachmentsState.modal.useSelectAttachment) {
            const item_id = $(this).data("item-id");
            selectAttachmentCard(item_id);
        }
    });
    const upload_btn_el = attachments_list_modal_el.find(".upload-btn");
    const upload_dz_el = attachments_list_modal_el.find(".upload-dropzone").dropzone({
        url: attachmentsData.upload.apiUrl,
        maxFiles: 1,
        acceptedFiles: "image/*",
        addRemoveLinks: !0,
        autoProcessQueue: false,
        init: function () {
            let files = 0
            this.on("addedfile", function (file) {
                files++
                if (!attachmentsState.upload.currentAttachmentFileValue && files === 1) {
                    attachmentsState.upload.currentAttachmentFileValue = file;
                    upload_btn_el.attr("disabled", false);
                }
            })
            this.on('removedfile', function (file) {
                files--
                if (files === 0) {
                    attachmentsState.upload.currentAttachmentFileValue = null;
                    upload_btn_el.attr("disabled", true);
                }
            });
            if (!attachmentsState.upload.currentAttachmentFileValue) {
                upload_btn_el.attr("disabled", true);
            }
        },
    });
    upload_btn_el.on("click", function () {
        const formData = new FormData();
        formData.append('content_type', attachmentsData.content_type);
        formData.append('object_id', attachmentsData.object_id);
        formData.append('attachment_type', "file");
        formData.append('file', attachmentsState.upload.currentAttachmentFileValue);
        attachmentsState.upload.isLoading = true;
        $.ajax({
            url: attachmentsData.upload.apiUrl,
            type: 'POST',
            data: formData,
            dataType: 'JSON',
            mimeType: "multipart/form-data",
            contentType: false,
            cache: false,
            processData: false,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", $("[name=csrfmiddlewaretoken]").attr("value"));
            },
            error: function () {
            },
            success: function (response) {
                upload_dz_el[0].dropzone.removeAllFiles();
                attachmentsState.upload.currentAttachmentFileValue = null;
                upload_btn_el.attr('disabled', true);
                loadAttachments();
            },
            always: function () {
                attachmentsState.upload.isLoading = false;
            },
        });
    });
    $(document).on("click", ".file-close", function (event) {
        event.preventDefault();
        const item_id = $($(this).closest(".file-man-box")).data("item-id");
        const selected_item = attachmentsState.attachmentsList.data.find(function (item) {
            return item.id === item_id;
        });
        if (!selected_item) {
            console.error("not found file item");
            return;
        }
        if (confirm("Are you sure to delete this file?")) {
            const formData = new FormData();
            formData.append('id', selected_item.id);
            attachmentsState.delete.isLoading = true;
            $.ajax({
                url: attachmentsData.row.delete.apiUrl,
                type: 'DELETE',
                data: formData,
                dataType: 'JSON',
                mimeType: "multipart/form-data",
                contentType: false,
                cache: false,
                processData: false,
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $("[name=csrfmiddlewaretoken]").attr("value"));
                },
                error: function () {
                },
                success: function (response) {
                    loadAttachments();
                },
                always: function () {
                    attachmentsState.delete.isLoading = false;
                }
            });
        }
    });

    thumbnailAttachmentWidgetsList.forEach(function (item) {
        const container_dz_el = item.thumbnail_img_preview_container_el.dropzone({
            url: attachmentsData.upload.apiUrl,
            maxFiles: 1,
            acceptedFiles: "image/*",
            addRemoveLinks: !0,
            autoProcessQueue: false,
            init: function () {
                let files = 0
                this.on("addedfile", function (file) {
                    files++
                    if (!item.formState.uploadAttachmentFile && files === 1) {
                        item.formState.uploadAttachmentFile = file;
                        item.thumbnail_img_preview_el.removeClass("active");
                        item.upload_btn_el.attr("disabled", false);
                    }
                })
                this.on('removedfile', function (file) {
                    files--
                    if (files === 0) {
                        item.formState.uploadAttachmentFile = null;
                        item.thumbnail_img_preview_el.addClass("active");
                        item.upload_btn_el.attr("disabled", true);
                    }
                });
            },
        });
        item.upload_btn_el.on("click", function () {
            fetchSaveRelatedObjectThumbnail(item, {
                success: function (response) {
                    container_dz_el[0].dropzone.removeAllFiles();
                }
            });
        });
        item.thumbnail_img_preview_el.on("click", function () {
            if (item.thumbnail_img_preview_el[0].classList.contains("active")) {
                container_dz_el[0].dropzone.hiddenFileInput.click();
            }
        });
        item.remove_btn_el.on("click", function () {
            fetchActionRelatedObject({
                attachment_type: "thumbnail_image",
                to_model_field_name: "thumbnail",
                action: "detach_related_single",
                obj_id: item.input_el.data("id"),
            }, {
                success: function () {
                    item.setInputValue();
                }
            });
        });
    });
});