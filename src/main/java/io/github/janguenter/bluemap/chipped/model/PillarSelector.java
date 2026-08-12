/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chipped.model;

/** Pure chain selector shared by the exact pillar-shaped loader families. */
public final class PillarSelector {

    private PillarSelector() {
    }

    public static PillarTextureRole select(boolean firstNeighbor, boolean secondNeighbor) {
        if (firstNeighbor && secondNeighbor) {
            return PillarTextureRole.CENTER;
        }
        if (firstNeighbor) {
            return PillarTextureRole.BOTTOM;
        }
        if (secondNeighbor) {
            return PillarTextureRole.TOP;
        }
        return PillarTextureRole.SELF;
    }
}
