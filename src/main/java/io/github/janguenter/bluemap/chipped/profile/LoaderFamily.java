/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chipped.profile;

import java.util.List;
import java.util.Locale;

/** Exact Athena loader families present in Chipped 4.0.2. */
public enum LoaderFamily {
    CTM("ctm", List.of("particle", "empty", "center", "vertical", "horizontal")),
    PILLAR("pillar", List.of("particle", "self", "top", "center", "bottom")),
    GIANT("giant", List.of("particle", "1", "2", "3", "4")),
    PANE_CTM("pane_ctm", List.of("particle", "empty", "center", "vertical", "horizontal")),
    CARPET_CTM("carpet_ctm", List.of("particle", "empty", "center", "vertical", "horizontal")),
    LIMITED_PILLAR(
            "limited_pillar", List.of("particle", "self", "top", "center", "bottom")
    ),
    PANE_PILLAR("pane_pillar", List.of("particle", "self", "top", "center", "bottom"));

    private final String wireName;
    private final List<String> textureRoles;

    LoaderFamily(String wireName, List<String> textureRoles) {
        this.wireName = wireName;
        this.textureRoles = textureRoles;
    }

    public String wireName() {
        return wireName;
    }

    public List<String> textureRoles() {
        return textureRoles;
    }

    public int textureIndex(String role) {
        int index = textureRoles.indexOf(role);
        if (index < 0) {
            throw new IllegalArgumentException("unsupported texture role: " + role);
        }
        return index;
    }

    public static LoaderFamily parse(String wireName) {
        String normalized = wireName.trim().toLowerCase(Locale.ROOT);
        for (LoaderFamily family : values()) {
            if (family.wireName.equals(normalized)) {
                return family;
            }
        }
        throw new IllegalArgumentException("unsupported loader family: " + wireName);
    }
}
