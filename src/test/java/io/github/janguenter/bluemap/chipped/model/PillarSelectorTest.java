/* SPDX-License-Identifier: MIT */
package io.github.janguenter.bluemap.chipped.model;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class PillarSelectorTest {

    @Test
    void exactFirstSecondTableIsNotInverted() {
        assertEquals(PillarTextureRole.SELF, PillarSelector.select(false, false));
        assertEquals(PillarTextureRole.BOTTOM, PillarSelector.select(true, false));
        assertEquals(PillarTextureRole.TOP, PillarSelector.select(false, true));
        assertEquals(PillarTextureRole.CENTER, PillarSelector.select(true, true));
    }

    @Test
    void axisNeighborOrderingAndCapsMatchExactContract() {
        assertEquals(new CubeFace.Vec(-1, 0, 0), PillarAxis.X.first());
        assertEquals(new CubeFace.Vec(1, 0, 0), PillarAxis.X.second());
        assertEquals(new CubeFace.Vec(0, 1, 0), PillarAxis.Y.first());
        assertEquals(new CubeFace.Vec(0, -1, 0), PillarAxis.Y.second());
        assertEquals(new CubeFace.Vec(0, 0, -1), PillarAxis.Z.first());
        assertEquals(new CubeFace.Vec(0, 0, 1), PillarAxis.Z.second());
        assertTrue(PillarAxis.X.isCap(CubeFace.WEST));
        assertTrue(PillarAxis.Y.isCap(CubeFace.UP));
        assertTrue(PillarAxis.Z.isCap(CubeFace.NORTH));
    }

    @Test
    void sideUvRotationsRemainBoundToAxesAndFaces() {
        assertEquals(1, PillarAxis.X.uvRotation(CubeFace.UP));
        assertEquals(1, PillarAxis.X.uvRotation(CubeFace.DOWN));
        assertEquals(1, PillarAxis.X.uvRotation(CubeFace.SOUTH));
        assertEquals(-1, PillarAxis.X.uvRotation(CubeFace.NORTH));
        assertEquals(0, PillarAxis.Y.uvRotation(CubeFace.SOUTH));
        assertEquals(0, PillarAxis.Z.uvRotation(CubeFace.UP));
        assertEquals(2, PillarAxis.Z.uvRotation(CubeFace.DOWN));
        assertEquals(-1, PillarAxis.Z.uvRotation(CubeFace.EAST));
        assertEquals(1, PillarAxis.Z.uvRotation(CubeFace.WEST));
    }

    @Test
    void axisDecoderAcceptsOnlyExactPersistedWireValues() {
        assertEquals(PillarAxis.X, PillarAxis.parse("x"));
        assertEquals(PillarAxis.Y, PillarAxis.parse("y"));
        assertEquals(PillarAxis.Z, PillarAxis.parse("z"));
        assertThrows(IllegalArgumentException.class, () -> PillarAxis.parse(" X "));
        assertThrows(IllegalArgumentException.class, () -> PillarAxis.parse(null));
    }
}
