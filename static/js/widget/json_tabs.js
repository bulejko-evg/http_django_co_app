class JsonFieldTabsManager {
    constructor(options) {
        this.key = options.key;
        this.tabLabels = document.querySelectorAll(`.tab__item-${options.key}`);
        this.tabContents = document.querySelectorAll(`.tab-content__item-${options.key}`);
        this.jsonTextarea = document.querySelector(`.json-textarea-${options.key}`);
        this.valuesStr = this.jsonTextarea.innerHTML;
        this.valuesObj = JSON.parse(this.valuesStr);
        this.tm;
        this.setup();
    }
    setup() {
        this.tabContents.forEach(tab => {
            tab.innerHTML = this.valuesObj[tab.dataset.item] || "";
        })
    }
    selectTab(elem) {
        var tabKey = elem.dataset.item;

        this.tabLabels.forEach(lb => {
            if (lb.dataset.item == tabKey) {
                lb.classList.add("select");
            } else {
                lb.classList.remove("select");
            }
        })
        this.tabContents.forEach(tab => {
            if (tab.dataset.item == tabKey) {
                tab.classList.remove("hidden");
            } else {
                tab.classList.add("hidden");
            }
        })
    }
    setContent(key, val) {
        let vals = JSON.parse(this.jsonTextarea.innerHTML);
        vals[key] = val;
        this.jsonTextarea.innerHTML = JSON.stringify(vals);
    }
    changeContent(elem) {
        var tabKey = elem.dataset.item;
        const tabContent = elem.value;
        clearTimeout(this.tm);
        this.tm = setTimeout(() => {
            this.setContent(tabKey, tabContent);
        }, "500");
    }
}
