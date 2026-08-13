/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chipped.adapter.bluemap522;

import de.bluecolored.bluemap.core.resources.pack.resourcepack.ResourcePack;
import de.bluecolored.bluemap.core.resources.pack.resourcepack.ResourcePackExtension;
import de.bluecolored.bluemap.core.resources.pack.resourcepack.blockstate.Variant;
import de.bluecolored.bluemap.core.resources.pack.resourcepack.blockstate.VariantSet;
import de.bluecolored.bluemap.core.resources.pack.resourcepack.blockstate.Variants;
import de.bluecolored.bluemap.core.resources.pack.resourcepack.model.Model;
import de.bluecolored.bluemap.core.resources.pack.resourcepack.texture.Texture;
import de.bluecolored.bluemap.core.util.Key;
import de.bluecolored.bluemap.core.world.BlockProperties;
import de.bluecolored.bluemap.core.world.BlockState;
import io.github.janguenter.bluemap.chipped.activation.ChippedRuntime;
import io.github.janguenter.bluemap.chipped.profile.Chipped402Athena406Profile;
import io.github.janguenter.bluemap.chipped.profile.ExactModArtifactDetector;
import io.github.janguenter.bluemap.chipped.profile.LoaderFamily;
import io.github.janguenter.bluemap.chipped.profile.ProfileDisablement;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;
import java.util.Set;

/** Exact artifact/schema activation and routing for the Chipped/Athena profile. */
final class ChippedResourceExtension implements ResourcePackExtension {

    private static final Key SYNTHETIC = Key.parse("bluemap_chipped:athena_shape");

    private final ResourcePack resourcePack;
    private final ChippedRuntime runtime;

    ChippedResourceExtension(ResourcePack resourcePack, ChippedRuntime runtime) {
        this.resourcePack = resourcePack;
        this.runtime = runtime;
    }

    @Override
    public void loadResources(Iterable<Path> roots) throws IOException, InterruptedException {
        if (ProfileDisablement.current().isDisabled(
                Chipped402Athena406Profile.PROFILE_ID
        )) {
            runtime.route().inactive("operator-disabled");
            return;
        }
        if (!ExactModArtifactDetector.matchesRequiredPair(roots)) {
            runtime.route().inactive("exact-artifact-pair-missing");
            return;
        }
        ActiveResourceSchemaValidator.Result schema = ActiveResourceSchemaValidator.validate(
                resourcePack, roots, Chipped402Athena406Profile.DEFINITIONS
        );
        if (!schema.valid()) {
            runtime.route().inactive(schema.reason());
            return;
        }
        de.bluecolored.bluemap.core.resources.pack.resourcepack.blockstate.BlockState dispatch =
                resourcePack.getBlockStates().get(SYNTHETIC);
        if (!validDispatch(dispatch)) {
            runtime.route().inactive("synthetic-dispatch-invalid");
            return;
        }
        runtime.route().activate();
    }

    @Override
    public Set<Key> collectUsedTextureKeys() {
        return runtime.route().isActive()
                ? Chipped402Athena406Profile.REQUIRED_TEXTURES
                : Set.of();
    }

    @Override
    public void bake() {
        if (!runtime.route().isActive()) {
            return;
        }
        for (Key texture : Chipped402Athena406Profile.REQUIRED_TEXTURES) {
            if (resourcePack.getTextures().get(texture) == null) {
                runtime.route().inactive("required-texture-missing");
                return;
            }
        }
    }

    @Override
    public Key getBlockStateKey(Key key) {
        return runtime.route().isActive()
                && Chipped402Athena406Profile.ROUTED_BLOCKS.contains(key.getFormatted())
                ? SYNTHETIC : key;
    }

    @Override
    public void getBlockProperties(BlockState blockState, BlockProperties.Builder builder) {
        if (!runtime.route().isActive()) {
            return;
        }
        io.github.janguenter.bluemap.chipped.profile.ChippedDefinition definition =
                Chipped402Athena406Profile.DEFINITIONS.get(
                        blockState.getId().getFormatted()
                );
        if (definition == null) {
            return;
        }
        if (definition.family() == LoaderFamily.PANE_CTM
                || definition.family() == LoaderFamily.PANE_PILLAR
                || definition.family() == LoaderFamily.CARPET_CTM) {
            builder.culling(false).occluding(false).cullingIdentical(false);
            return;
        }
        Model originalModel = resourcePack.getModels().get(Key.parse(definition.modelId()));
        if (originalModel != null) {
            // Routing swaps in a synthetic dispatch model. Preserve the active
            // full-cube model's alpha-sensitive culling result. All owned
            // ordinary models are full cube_all/cube_column shapes, so a
            // non-culling result means an active translucent texture and must
            // also be non-occluding (BlueMap's generic model property alone
            // treats every full cube as occluding regardless of alpha).
            List<Texture> roleTextures = definition.textures().stream()
                    .map(Key::parse)
                    .map(resourcePack.getTextures()::get)
                    .toList();
            boolean opaqueFullCube = opaqueFullCube(
                    originalModel.isCulling(), roleTextures
            );
            builder.culling(opaqueFullCube)
                    .occluding(opaqueFullCube)
                    .cullingIdentical(false);
        }
    }

    static boolean opaqueFullCube(
            boolean originalModelCulling,
            List<Texture> roleTextures
    ) {
        return originalModelCulling
                && !roleTextures.isEmpty()
                && roleTextures.stream().allMatch(texture ->
                        texture != null && texture.getColorStraight().a >= 1F
                );
    }

    private static boolean validDispatch(
            de.bluecolored.bluemap.core.resources.pack.resourcepack.blockstate.BlockState state
    ) {
        if (state == null || state.getMultipart() != null) {
            return false;
        }
        Variants variants = state.getVariants();
        if (variants == null || variants.getDefaultVariant() == null) {
            return false;
        }
        VariantSet set = variants.getDefaultVariant();
        if (set.getVariants().length != 1) {
            return false;
        }
        Variant variant = set.getVariants()[0];
        return BlueMap522Adapter.isExpectedDispatch(variant);
    }
}
