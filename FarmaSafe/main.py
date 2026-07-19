from interfaz.panel_principal import PanelPrincipal


#inicia la ventana principal del sistema
if __name__ == "__main__":
    aplicacion = PanelPrincipal()
    aplicacion.protocol(
        "WM_DELETE_WINDOW",
        aplicacion.cerrar_aplicacion
    )
    aplicacion.mainloop()