/* SPDX-License-Identifier: MIT */
package io.github.janguenter.bluemap.chipped.adapter.bluemap522;

import static org.junit.jupiter.api.Assertions.assertEquals;

import io.github.janguenter.bluemap.resource.athena.model.CubeFace;
import org.junit.jupiter.api.Test;

class ChippedRendererMappingTest {

    @Test
    void paneClockwiseTableMatchesExactHorizontalContract() {
        assertEquals(CubeFace.EAST, ChippedRenderer.clockwise(CubeFace.NORTH));
        assertEquals(CubeFace.WEST, ChippedRenderer.counterClockwise(CubeFace.NORTH));
        assertEquals(CubeFace.WEST, ChippedRenderer.clockwise(CubeFace.SOUTH));
        assertEquals(CubeFace.EAST, ChippedRenderer.counterClockwise(CubeFace.SOUTH));
        assertEquals(CubeFace.NORTH, ChippedRenderer.clockwise(CubeFace.WEST));
        assertEquals(CubeFace.SOUTH, ChippedRenderer.counterClockwise(CubeFace.WEST));
        assertEquals(CubeFace.SOUTH, ChippedRenderer.clockwise(CubeFace.EAST));
        assertEquals(CubeFace.NORTH, ChippedRenderer.counterClockwise(CubeFace.EAST));
    }
}
