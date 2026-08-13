/* SPDX-License-Identifier: MIT */
package io.github.janguenter.bluemap.chipped.adapter.bluemap522;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import de.bluecolored.bluemap.core.resources.pack.resourcepack.texture.Texture;
import de.bluecolored.bluemap.core.util.Key;
import java.awt.image.BufferedImage;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

class ChippedResourceExtensionTest {

    @Test
    void pixelOverrideAlphaCanOnlyMakeFullCubePropertiesMoreConservative()
            throws Exception {
        Texture opaque = Texture.MISSING;
        BufferedImage translucentPixel = new BufferedImage(
                1, 1, BufferedImage.TYPE_INT_ARGB
        );
        translucentPixel.setRGB(0, 0, 0x80FFFFFF);
        Texture translucent = Texture.from(
                Key.parse("test:translucent-role"), translucentPixel
        );
        List<Texture> opaqueRoles = List.of(opaque, opaque, opaque, opaque, opaque);

        assertTrue(ChippedResourceExtension.opaqueFullCube(true, opaqueRoles));
        assertFalse(ChippedResourceExtension.opaqueFullCube(false, opaqueRoles));

        List<Texture> overriddenRoles = new ArrayList<>(opaqueRoles);
        overriddenRoles.set(3, translucent);
        assertFalse(ChippedResourceExtension.opaqueFullCube(true, overriddenRoles));
        overriddenRoles.set(3, null);
        assertFalse(ChippedResourceExtension.opaqueFullCube(true, overriddenRoles));
    }
}
