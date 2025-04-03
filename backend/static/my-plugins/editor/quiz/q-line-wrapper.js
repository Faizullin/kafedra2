class QLineWrapper {
    static get toolbox() {
        return {
            title: 'Q Line Wrapper',
            icon: '<svg width="17" height="15" viewBox="0 0 336 276" xmlns="http://www.w3.org/2000/svg"><path d="M291 150V79c0-19-15-34-34-34H79c-19 0-34 15-34 34v42l67-44 81 72 56-29 42 30zm0 52l-43-30-56 30-81-67-66 39v23c0 19 15 34 34 34h178c17 0 31-13 34-29zM79 0h178c44 0 79 35 79 79v118c0 44-35 79-79 79H79c-44 0-79-35-79-79V79C0 35 35 0 79 0z"/></svg>'
        };
    }

    constructor({ data, api }) {
        this.api = api;
        this.data = {
            text: data.text || '',
            blocks: data.blocks || []
        };
        this.wrapper = undefined;
    }

    render() {
        this.wrapper = document.createElement('div');
        this.wrapper.classList.add('qline-wrapper');
        
        const textLine = document.createElement('div');
        textLine.contentEditable = true;
        textLine.classList.add('qline-text');
        textLine.innerHTML = this.data.text;
        textLine.addEventListener('input', () => {
            this.data.text = textLine.innerHTML;
        });
        
        this.wrapper.appendChild(textLine);
        
        const addQuestionBtn = document.createElement('button');
        addQuestionBtn.innerText = 'Add Question';
        addQuestionBtn.classList.add('qline-add-question');
        addQuestionBtn.addEventListener('click', () => this.addQuestionBlock());
        
        this.wrapper.appendChild(addQuestionBtn);
        
        this.data.blocks.forEach(block => this.addQuestionBlock(block));
        
        return this.wrapper;
    }

    addQuestionBlock(data = { type: 'short_answer', content: '' }) {
        const questionBlock = document.createElement('div');
        questionBlock.classList.add('qline-question');
        
        const select = document.createElement('select');
        select.innerHTML = `
            <option value="short_answer">Short Answer</option>
            <option value="true_false">True/False</option>
        `;
        select.value = data.type;
        select.addEventListener('change', (e) => {
            data.type = e.target.value;
            this.updateQuestionBlock(questionBlock, data);
        });
        
        questionBlock.appendChild(select);
        
        this.updateQuestionBlock(questionBlock, data);
        
        this.wrapper.appendChild(questionBlock);
        this.data.blocks.push(data);
    }

    updateQuestionBlock(block, data) {
        let input = block.querySelector('.qline-input');
        if (input) block.removeChild(input);
        
        if (data.type === 'short_answer') {
            input = document.createElement('input');
            input.type = 'text';
            input.classList.add('qline-input');
            input.value = data.content;
            input.placeholder = 'Short Answer';
        } else {
            input = document.createElement('select');
            input.classList.add('qline-input');
            input.innerHTML = `
                <option value="true">True</option>
                <option value="false">False</option>
            `;
            input.value = data.content;
        }
        
        input.addEventListener('input', (e) => {
            data.content = e.target.value;
        });
        
        block.appendChild(input);
    }

    save(blockContent) {
        return this.data;
    }
}
