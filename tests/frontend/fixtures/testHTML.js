<div data-screen="home" style="display: none;">
    Home screen
    <a href="/static/cartera_isin.html?selected_screen=settings">settings</a>
</div>

<div data-screen="cartera_accion" class="cartera" style="display: none;">
    <p class="c-loading" style="display: none;">Loading cartera…</p>
    <p class="c-error" style="display: none;"></p>

    <div class="cartera-content" style="display: none;">
        <div>
            <div>
                <h2 class="accion-nombre"></h2>
                <p class="muted">
                    ISIN: <span class="accion-isin"></span>
                </p>
            </div>

            <section>
                <h3>Operaciones</h3>

                <table class="c-table">
                    <thead>
                        <tr>
                            <th>Fecha</th>
                            <th>Tipo</th>
                            <th>Cantidad</th>
                            <th>divisa</th>
                            <th>Precio</th>
                            <th>Importe</th>
                            <th>Broker</th>
                            <th>Dias Ultima Venta</th>
                            <th>Restantes</th>
                        </tr>
                    </thead>
                    <tbody class="operaciones-tbody">
                    </tbody>
                </table>
                <p>
                    Acciones actual <b class="acciones-actual"></b> Valor: <b class="valor-actual"></b>
                </p>
            </section>

            <section>
                <h3>Compras y Ventas Asociadas</h3>
                <div class="compra-ventas-container"></div>
            </section>

            <section>
                <h3>Dividendos</h3>
                <table class="c-table" border="1">
                <thead>
                    <tr>
                        <th>Concepto</th>
                        <th>Fecha</th>
                        <th>Importe €</th>
                    </tr>
                </thead>
                <tbody class="dividendos-tbody">
                </tbody>
                </table>
            </section>
        </div>
    </div>
</div>

<div data-screen="year_report" class="year_report" style="display: none;">
    <p class="c-loading" style="display: none;">Loading…</p>
    <p class="c-error" style="display: none;"></p>

    <div class="year-content" style="display: none;">
        <section class="content">
            <h1 class="year-title"></h1>
            <table class="c-table" border="1">
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Compra Fecha</th>
                        <th>Precio Unitario Compra</th>
                        <th>Venta Fecha</th>
                        <th>Precio Unitario Venta</th>
                        <th>Beneficio €</th>
                    </tr>
                </thead>
                <tbody class="compra-ventas-tbody">
                </tbody>
            </table>

            <table class="c-table" border="1">
                <thead>
                    <tr>
                        <th>Concepto</th>
                        <th>Fecha</th>
                        <th>Importe €</th>
                    </tr>
                </thead>
                <tbody class="dividendos-tbody">
                </tbody>
            </table>
        </section>
    </div>
</div>

<div data-screen="no_screen" style="display: none;">
    No screen
</div>

<div id="acciones-list"></div>
