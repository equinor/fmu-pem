---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: FMU PEM
  text: "User documentation"
  tagline: Calculate seismic properties from rock physics models in a FMU context.
  actions:
    - theme: brand
      text: Why and how PEM?
      link: ./use-cases
    - theme: brand
      text: ERT configuration
      link: /ert-configuration
    - theme: brand
      text: PEM configuration
      link: /pem-configuration

features:
  - icon: 🛠️
    title: Less maintenance
    details: No need for custom scripts in your FMU or RMS project. PEM is maintained centrally by Equinor, and available as pre-installed ERT forward models.
  - icon: 🤝
    title: Shared rock physics library
    details: FMU PEM uses the same underlying rock physics library as RokDoc plugins - ensuring consistent output across the software portfolio.
---
