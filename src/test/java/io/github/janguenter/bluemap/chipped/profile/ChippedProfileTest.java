/* SPDX-License-Identifier: MIT */
package io.github.janguenter.bluemap.chipped.profile;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.EnumMap;
import java.util.Map;
import org.junit.jupiter.api.Test;

class ChippedProfileTest {

    @Test
    void exactMetadataOnlyCatalogHasClosedSevenFamilyRoster() {
        assertEquals(1_427, Chipped402Athena406Profile.DEFINITIONS.size());
        assertEquals(5_947, Chipped402Athena406Profile.REQUIRED_TEXTURES.size());
        Map<LoaderFamily, Integer> counts = new EnumMap<>(LoaderFamily.class);
        Chipped402Athena406Profile.DEFINITIONS.values().forEach(
                definition -> counts.merge(definition.family(), 1, Integer::sum)
        );
        assertEquals(Map.of(
                LoaderFamily.CTM, 896,
                LoaderFamily.PILLAR, 248,
                LoaderFamily.GIANT, 108,
                LoaderFamily.PANE_CTM, 93,
                LoaderFamily.CARPET_CTM, 48,
                LoaderFamily.LIMITED_PILLAR, 17,
                LoaderFamily.PANE_PILLAR, 17
        ), counts);
        assertTrue(Chipped402Athena406Profile.ROUTED_BLOCKS.stream()
                .allMatch(block -> block.startsWith("chipped:")));
    }
}
