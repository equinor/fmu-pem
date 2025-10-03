import {readFileSync} from "fs"
import {defineConfig} from 'vitepress'

// Copied from https://github.com/equinor/vscode-lang-ert/blob/master/syntaxes/ert.tmLanguage.json
const ertLanguageGrammar = JSON.parse(readFileSync("./docs/ert.tmLanguage.json"))

// https://vitepress.dev/reference/site-config
export default defineConfig({
    title: "FMU PEM",
    description: "User documentation for using fmu-pem",
    head: [
        ["link", {rel: "stylesheet", href: "https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css"}]
    ],
    markdown: {
        math: true,
        languages: [ertLanguageGrammar]
    },
    themeConfig: {
        // https://vitepress.dev/reference/default-theme-config
        nav: [
            {text: 'Home', link: '/'},
        ],
        logo: {light: "/fmu_logo_light_mode.svg", dark: "/fmu_logo_dark_mode.svg"},
        sidebar: [
            {
                text: 'Setup',
                items: [
                    {
                        text: "fmu-PEM manual", link: "/use-cases", items: [
                            {text: 'Read and validate YAML file', link: '/yaml-validation'},
                            {text: 'Import reservoir simulator results', link: '/import-sim-results'},
                            {text: 'Estimate effective mineral properties', link: '/effective-mineral-properties'},
                            {text: 'Estimate effective fluid properties', link: '/fluid-properties'},
                            {text: 'Estimate effective pressure', link: '/effective-pressure'},
                            {text: 'Estimate saturated rock properties', link: '/saturated-rock'},
                            {text: '(Optional) estimate difference properties', link: '/difference-properties'},
                            {text: 'Save intermediate (optional) and final estimates', link: '/save-results'},
                            {text: 'Model file formats', link: '/model-file-formats'},
                        ]
                    },
                    {text: 'ERT configuration', link: '/ert-configuration'},
                    {text: 'PEM configuration', link: '/pem-configuration'}
                ]
            }
        ],
        socialLinks: [
            {icon: 'github', link: 'https://github.com/equinor/fmu-pem'}
        ]
    },
    ignoreDeadLinks: true
})
