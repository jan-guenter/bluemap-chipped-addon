/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chipped.profile;

import de.bluecolored.bluemap.core.util.Key;

import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

/** Exact All the Mons 1.2.0 Chipped/Athena profile. */
public final class Chipped402Athena406Profile {

    public static final String PROFILE_ID = "chipped-athena-4.0.2-4.0.6";
    public static final String CHIPPED_SHA256 =
            "18ac6fd6b30db4922ccc6ee8bea5b113f69587505b7529834f37ace506427291";
    public static final long CHIPPED_SIZE = 15_020_578L;
    public static final String ATHENA_SHA256 =
            "43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5";
    public static final long ATHENA_SIZE = 99_944L;
    public static final int ROUTED_BLOCK_COUNT = 1_427;
    public static final int REQUIRED_TEXTURE_COUNT = 5_947;
    public static final String DEFINITIONS_SHA256 =
            "1ce109e515e89e5d73ebb796cfdb84f49c57e52a97a1c6b0a95e2bc80777ca7a";

    public static final DefinitionCatalog CATALOG = DefinitionCatalog.load(
            "/bluemap-chipped/profiles/chipped/4.0.2-athena-4.0.6/definitions.tsv",
            ROUTED_BLOCK_COUNT,
            DEFINITIONS_SHA256
    );
    public static final Map<String, ChippedDefinition> DEFINITIONS = CATALOG.definitions();
    public static final Set<String> ROUTED_BLOCKS = DEFINITIONS.keySet();
    public static final Set<Key> REQUIRED_TEXTURES = CATALOG.textureIds().stream()
            .map(Key::parse)
            .collect(Collectors.toUnmodifiableSet());

    static {
        if (REQUIRED_TEXTURES.size() != REQUIRED_TEXTURE_COUNT) {
            throw new IllegalStateException("required texture roster changed");
        }
    }

    private Chipped402Athena406Profile() {
    }
}
