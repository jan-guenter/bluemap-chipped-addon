/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chipped.activation;

/** Process-scoped state for the single exact Chipped/Athena route. */
public final class ChippedRuntime {

    public static final String ROUTE_ID = "chipped-athena-4.0.2-4.0.6";
    public static final ChippedRuntime INSTANCE = new ChippedRuntime();

    private final RouteActivation route = new RouteActivation(ROUTE_ID);

    private ChippedRuntime() {
    }

    public RouteActivation route() {
        return route;
    }

    public void disable(String detail) {
        route.fail(detail);
    }
}
