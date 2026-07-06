declare module 'vue3-leaflet' {
  import type { DefineComponent } from 'vue'

  export const LMap: DefineComponent<{}, {}, any>
  export const LTileLayer: DefineComponent<{}, {}, any>
  export const LMarker: DefineComponent<{}, {}, any>
  export const LPopup: DefineComponent<{}, {}, any>
}
