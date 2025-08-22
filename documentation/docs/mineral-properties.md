# Effective mineral properties

The solid part of a rock, often called the rock matrix, will generally consist of a mix of minerals, each
having a volume fraction. We are interested in knowing the effective properties of the rock for each cell in the
grid. To achieve this, we must know the properties of each mineral, and then have an effective media model which
tells us how to combine the mineral properties.

By mineral properties we mean density, bulk modulus and shear modulus, as these are the elastic properties required
in an **isotropic** case.

*Table 1: Key physical properties of minerals required for isotropic elastic modelling*

| Property      | Unit    | Explanation                          |
| ------------- | ------- | ------------------------------------ |
| Density       | kg/m^3  | Mass divided by volume               |
| Bulk modulus  | Pa      | Resistance against change in volume  |
| Shear modulus | Pa      | Resistance against change in shape   |

The YAML config file will contain definitions of elastic properties for a series of common minerals. More can be
found e.g. in the [Rock Physics Handbook][^1].


## References

[^1]: Mavko, G., Mukerji, T., & Dvorkin, J. (2020). *The Rock Physics Handbook* (3rd ed.). Cambridge University Press.
