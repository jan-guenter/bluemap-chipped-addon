/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chipped.adapter.bluemap522;

import de.bluecolored.bluemap.core.resources.pack.resourcepack.ResourcePack;
import de.bluecolored.bluemap.core.util.Key;
import io.github.janguenter.bluemap.chipped.activation.ChippedRuntime;

/** Resource-pack extension factory registered before resource loading begins. */
final class ChippedResourceExtensionType
        implements ResourcePack.Extension<ChippedResourceExtension> {

    static final Key KEY = Key.parse("bluemap_chipped:exact_profile");

    private final ChippedRuntime runtime;

    ChippedResourceExtensionType(ChippedRuntime runtime) {
        this.runtime = runtime;
    }

    @Override
    public Key getKey() {
        return KEY;
    }

    @Override
    public ChippedResourceExtension create(ResourcePack pack) {
        return new ChippedResourceExtension(pack, runtime);
    }
}
