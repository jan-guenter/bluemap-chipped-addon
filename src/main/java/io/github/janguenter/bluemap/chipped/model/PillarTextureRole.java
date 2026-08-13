/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chipped.model;

/** Stable chain-position texture in an Athena pillar family. */
public enum PillarTextureRole {
    PARTICLE("particle"),
    SELF("self"),
    TOP("top"),
    CENTER("center"),
    BOTTOM("bottom");

    private final String wireName;

    PillarTextureRole(String wireName) {
        this.wireName = wireName;
    }

    public String wireName() {
        return wireName;
    }
}
