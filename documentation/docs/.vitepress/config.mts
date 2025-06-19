import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "FMU PEM",
  description: "User documentation for using fmu-pem",
  head: [
    ["link", { rel: "stylesheet", href: "https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css"}]
  ],
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
    ],
    logo: { light: "/fmu_logo_light_mode.svg", dark: "/fmu_logo_dark_mode.svg"},
    sidebar: [
      {
        text: 'Setup',
        items: [
          { text: 'ERT configuration', link: '/ert-configuration' },
          { text: 'PEM configuration', link: '/pem-configuration' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/equinor/fmu-pem' }
    ]
  }
})
