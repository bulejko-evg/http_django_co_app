const themes = {
    light: {
        "--bg-html-color": "#FFFFFF",
        "--bg-body-color": "#FFFFFF",
        "--text-color": "#404040",
    },
    dark: {
        "--bg-html-color": "#FFFFFF",
        "--bg-body-color": "#C0C0C0",
        "--text-color": "#F0F0F0",
    }
}

class ThemeManager {
    /* html add data-theme */
    constructor(options) {
        this.docStyle = document.documentElement.style;
        this.themeElem = document.querySelector("html");
        this.themes = options.themes;
        this.theme = this.themeElem.dataset.theme || options.default;
        this.setup();
    }
    setup() {
        let themeKey = localStorage.getItem("theme");
        if (themeKey != null && themeKey != this.theme) {
            this.theme = themeKey;
            this.set(this.theme);
        }
    }
    getValidThemeKey(key) {
        let themeKey = key
        const themesKeys = Object.keys(this.themes)
        if (!themesKeys.includes(key)) {
            themeKey = themesKeys[0]
        }
        return themeKey
    }
    set(key) {
        let themeKey = this.getValidThemeKey(key)
        Object.entries(this.themes[themeKey]).forEach(([k, val]) => {
            this.docStyle.setProperty(k, val);
        });
    }
    get() {
        return this.theme;
    }
    next() {
        /* If theme key is null - get next obj from themes obj */
        const themesKeys = Object.keys(this.themes);
        let themeInd = themesKeys.indexOf(this.theme);
        const nextInd = (themeInd + 1) % themesKeys.length;
        return themesKeys[nextInd];
    }
    to(key=null) {
        if (this.theme == key) {return;}
        const themeKey = (key == null)? this.next() : key;
        this.set(themeKey);
        this.themeElem.setAttribute("data-theme", themeKey);
        localStorage.setItem("theme", themeKey);
        this.theme = themeKey;
        this.changeIcon(themeKey);
    }
    changeIcon(key) {
        icons = document.querySelectorAll(".theme");
        icons.foreEach(el => {
            if (el.id == "theme_" + key) {
                el.classList.add("hidden")
            } else {
                el.classList.remove("hidden")
            }
        })
    }
}
const theme = new ThemeManager({
    themes: themes,
    default: "light",
})
