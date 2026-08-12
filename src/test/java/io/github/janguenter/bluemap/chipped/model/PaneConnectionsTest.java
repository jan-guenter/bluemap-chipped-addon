/* SPDX-License-Identifier: MIT */
package io.github.janguenter.bluemap.chipped.model;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.Map;
import org.junit.jupiter.api.Test;

class PaneConnectionsTest {

    @Test
    void requiresAllFourExactPersistedBooleans() {
        PaneConnections connections = PaneConnections.parse(Map.of(
                "north", "true", "east", "false", "south", "true", "west", "false"
        ));
        assertEquals(new PaneConnections(true, false, true, false), connections);
        assertThrows(IllegalArgumentException.class, () -> PaneConnections.parse(Map.of()));
        assertThrows(IllegalArgumentException.class, () -> PaneConnections.parse(Map.of(
                "north", "1", "east", "false", "south", "false", "west", "false"
        )));
    }
}
