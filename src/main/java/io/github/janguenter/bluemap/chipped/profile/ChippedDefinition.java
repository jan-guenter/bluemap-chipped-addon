/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chipped.profile;

import java.util.List;
import java.util.Objects;

/** Metadata-only rendering definition derived from the exact installed JSON schema. */
public record ChippedDefinition(
        String blockId,
        LoaderFamily family,
        String modelId,
        String modelParent,
        List<String> textures,
        String modelTextureMapSha256
) {

    public ChippedDefinition {
        Objects.requireNonNull(blockId, "blockId");
        Objects.requireNonNull(family, "family");
        Objects.requireNonNull(modelId, "modelId");
        Objects.requireNonNull(modelParent, "modelParent");
        textures = List.copyOf(textures);
        Objects.requireNonNull(modelTextureMapSha256, "modelTextureMapSha256");
        if (!blockId.startsWith("chipped:")
                || textures.size() != family.textureRoles().size()
                || !modelTextureMapSha256.matches("[0-9a-f]{64}")) {
            throw new IllegalArgumentException("malformed Chipped rendering definition");
        }
    }

    public String texture(String role) {
        return textures.get(family.textureIndex(role));
    }
}
