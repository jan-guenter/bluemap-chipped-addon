/* SPDX-License-Identifier: MIT */
package io.github.janguenter.bluemap.chipped;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Modifier;
import org.junit.jupiter.api.Test;

class BlueMapChippedAddonTest {

    @Test
    void selectsOnlyTheAuditedFeatureBackportIdentity() {
        assertTrue(BlueMapChippedAddon.runtimeSupported(
                "5.22-feature.backport-5.23-stateless-java-web-server-46",
                "7e07f4e74ec1e92a6ead9aa1e66054af3e133aac"
        ));
        assertFalse(BlueMapChippedAddon.runtimeSupported(
                "5.22",
                "fe5115d5548a30d34175b8e0449aaca280af199f"
        ));
    }

    @Test
    void reflectionBoundaryFindsTheRenamedPublicInstallMethod() throws Exception {
        Class<?> adapter = BlueMapChippedAddon.loadAdapter(false);

        assertEquals(
                "io.github.janguenter.bluemap.chipped.adapter.bluemap523.BlueMap523Adapter",
                adapter.getName()
        );
        assertTrue(Modifier.isStatic(adapter.getMethod("install").getModifiers()));
        assertTrue(Modifier.isPublic(adapter.getMethod("install").getModifiers()));
    }

}
