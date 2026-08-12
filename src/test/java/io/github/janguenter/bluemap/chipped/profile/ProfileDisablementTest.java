/* SPDX-License-Identifier: MIT */
package io.github.janguenter.bluemap.chipped.profile;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Set;
import org.junit.jupiter.api.Test;

class ProfileDisablementTest {

    @Test
    void propertyAndEnvironmentValuesMergeCanonically() {
        ProfileDisablement disabled = ProfileDisablement.from(
                " Chipped-Athena-4.0.2-4.0.6,INVALID VALUE ",
                "future,chipped-athena-4.0.2-4.0.6"
        );
        assertEquals(
                Set.of("chipped-athena-4.0.2-4.0.6", "future"),
                disabled.disabledProfiles()
        );
        assertTrue(disabled.isDisabled("CHIPPED-ATHENA-4.0.2-4.0.6"));
        assertFalse(disabled.isDisabled("missing"));
    }
}
