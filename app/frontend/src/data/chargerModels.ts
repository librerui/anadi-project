// Catalogue of real, commercially available EV charger models commonly deployed
// in Portugal / the EU. Power ratings and connector types reflect the
// manufacturers' public datasheets. Illustrations are generic pictograms
// (wallbox vs. pedestal/DC pillar) rather than branded product photography,
// since we cannot bundle copyrighted manufacturer images in the app bundle.
export type ChargerType = 'AC' | 'DC'

export interface ChargerModel {
  id: string
  brand: string
  model: string
  power: number // kW
  type: ChargerType
  connector: string
  icon: 'wallbox' | 'pedestal' | 'pillar'
}

export const chargerModels: ChargerModel[] = [
  {
    id: 'wallbox-pulsar-plus-7_4',
    brand: 'Wallbox',
    model: 'Pulsar Plus',
    power: 7.4,
    type: 'AC',
    connector: 'Type 2',
    icon: 'wallbox',
  },
  {
    id: 'schneider-evlink-home-7_4',
    brand: 'Schneider Electric',
    model: 'EVlink Home',
    power: 7.4,
    type: 'AC',
    connector: 'Type 2',
    icon: 'wallbox',
  },
  {
    id: 'abb-terra-ac-22',
    brand: 'ABB',
    model: 'Terra AC',
    power: 22.0,
    type: 'AC',
    connector: 'Type 2',
    icon: 'pedestal',
  },
  {
    id: 'circutor-rve-22',
    brand: 'Circutor',
    model: 'RVE Smart',
    power: 22.0,
    type: 'AC',
    connector: 'Type 2',
    icon: 'pedestal',
  },
  {
    id: 'efacec-qc45-50',
    brand: 'Efacec',
    model: 'QC45',
    power: 50.0,
    type: 'DC',
    connector: 'CCS / CHAdeMO',
    icon: 'pillar',
  },
  {
    id: 'abb-terra-184-180',
    brand: 'ABB',
    model: 'Terra 184',
    power: 180.0,
    type: 'DC',
    connector: 'CCS',
    icon: 'pillar',
  },
]

export const getChargerModel = (id: string): ChargerModel | undefined =>
  chargerModels.find((c) => c.id === id)
