class QuestionFormManager {
    constructor(options) {
        if (!options.question) {
            throw new Error("Question object is required");
        }
        if (!options.holder) {
            throw new Error("Holder element is required");
        }
        this.question = options.question;
        this.steps = options.steps || [];
        this.currentStep = this.steps[0] || null;
        this.loadedForms = {};
        this.loadingStates = {};

        this.formContainerEl = $(options.holder);
        this.tabsEl = this.formContainerEl.find(".nav-link");

        this.init();
    }

    init() {
        this.updateAvailableTabs();
        if (this.currentStep) {
            this.loadForm(this.currentStep);
        }

        this.tabsEl.click((e) => this.handleTabClick(e));
        $(document).on("submit", ".dynamic-form", (e) => this.handleFormSubmit(e));
        $(document).on("change", ".dynamic-form .my-question-type-field", (e) => this.updateQuestionType(e));
    }

    handleTabClick(event) {
        event.preventDefault();
        let newStep = $(event.target).data("step");

        if (newStep !== this.currentStep) {
            this.currentStep = newStep;
            this.updateActiveTab();
            this.loadForm(this.currentStep);
        }
    }

    updateActiveTab() {
        this.tabsEl.removeClass("active");
        this.tabsEl.filter(`[data-step='${this.currentStep}']`).addClass("active");
    }

    loadForm(step) {
        if (this.loadingStates[step]) return;
        this.loadingStates[step] = true;

        if (this.loadedForms[step]) {
            this.formContainerEl.html(this.loadedForms[step]);
            this.loadingStates[step] = false;
            return;
        }

        const action_url = window.managers.urlFormatter.formatUrlById(this.question, window.server_conf.urls.questionEditorApi, {
            step: step,
            question_type: this.questionType,
        });
        $.ajax({
            url: action_url,
            type: "GET",
            success: (response) => {
                if (response.success) {
                    this.loadedForms[step] = response.form;
                    this.formContainerEl.html(response.form);
                } else {
                    this.formContainerEl.html(`<div class="alert alert-danger">${response.error}</div>`);
                }
                this.loadingStates[step] = false;
            },
            error: () => {
                this.formContainerEl.html(`<div class="alert alert-danger">Error loading form</div>`);
                this.loadingStates[step] = false;
            }
        });
    }

    handleFormSubmit(event) {
        event.preventDefault();
        let form = $(event.target);
        let formData = form.serialize();

        const action_url = window.managers.urlFormatter.formatUrlById(this.question, window.server_conf.urls.questionEditorApi, {
            step: this.currentStep,
        });
        $.ajax({
            url: action_url,
            type: "POST",
            data: formData,
            success: (response) => {
                if (response.success) {
                    alert("Form saved successfully!");
                    this.loadedForms[this.currentStep] = null;
                    this.loadForm(this.currentStep);
                } else {
                    this.formContainerEl.html(response.form);
                }
            },
            error: () => {
                alert("Error submitting form");
            }
        });
    }

    updateQuestionType(options) {
        this.questionType = options.questionType;
        this.steps = options.steps || [];
        this.currentStep = this.steps[0] || null;
        this.loadedForms = {};
        this.loadingStates = {};

        this.updateAvailableTabs();
        if (this.currentStep) {
            this.loadForm(this.currentStep);
        }
    }

    updateAvailableTabs() {
        this.tabsEl.parent().hide();
        this.steps.forEach((step) => {
            this.tabsEl.filter(`[data-step='${step}']`).parent().show();
        });
        this.updateActiveTab();
    }
}

window.managers.addInstance("questionEditor", QuestionFormManager());