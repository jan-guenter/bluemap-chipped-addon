/* SPDX-License-Identifier: MIT */
package io.github.janguenter.bluemap.chipped.profile;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class ExactModArtifactDetectorTest {

    @Test
    void onlyTheExactInstalledPairActivates() {
        String chippedValue = System.getProperty("chippedJar");
        String athenaValue = System.getProperty("athenaJar");
        if (chippedValue == null || athenaValue == null) {
            return;
        }
        Path chipped = Path.of(chippedValue);
        Path athena = Path.of(athenaValue);
        if (!Files.isRegularFile(chipped) || !Files.isRegularFile(athena)) {
            return;
        }
        assertTrue(ExactModArtifactDetector.matchesRequiredPair(List.of(chipped, athena)));
        assertFalse(ExactModArtifactDetector.matchesRequiredPair(List.of(chipped)));
        assertFalse(ExactModArtifactDetector.matches(
                List.of(chipped, athena),
                Map.of(
                        "chipped", new ExactModArtifactDetector.Identity(
                                Chipped402Athena406Profile.CHIPPED_SHA256,
                                Chipped402Athena406Profile.CHIPPED_SIZE + 1
                        ),
                        "athena", new ExactModArtifactDetector.Identity(
                                Chipped402Athena406Profile.ATHENA_SHA256,
                                Chipped402Athena406Profile.ATHENA_SIZE
                        )
                )
        ));
    }
}
