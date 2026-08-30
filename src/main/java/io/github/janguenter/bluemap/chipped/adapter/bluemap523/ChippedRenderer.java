/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chipped.adapter.bluemap523;

import de.bluecolored.bluemap.core.map.TextureGallery;
import de.bluecolored.bluemap.core.map.hires.MaxCapacityReachedException;
import de.bluecolored.bluemap.core.map.hires.RenderSettings;
import de.bluecolored.bluemap.core.map.hires.TileModelView;
import de.bluecolored.bluemap.core.map.hires.block.BlockRenderer;
import de.bluecolored.bluemap.core.map.hires.block.ResourceModelRenderer;
import de.bluecolored.bluemap.core.resources.pack.resourcepack.ResourcePack;
import de.bluecolored.bluemap.core.resources.pack.resourcepack.blockstate.Variant;
import de.bluecolored.bluemap.core.util.Key;
import de.bluecolored.bluemap.core.util.math.Color;
import de.bluecolored.bluemap.core.world.BlockState;
import de.bluecolored.bluemap.core.world.block.BlockNeighborhood;
import de.bluecolored.bluemap.core.world.block.ExtendedBlock;
import io.github.janguenter.bluemap.chipped.activation.ChippedRuntime;
import io.github.janguenter.bluemap.resource.athena.model.CtmConnections;
import io.github.janguenter.bluemap.resource.athena.model.CtmTextureRole;
import io.github.janguenter.bluemap.resource.athena.model.CubeFace;
import io.github.janguenter.bluemap.chipped.model.GiantTextureSelector;
import io.github.janguenter.bluemap.chipped.model.PaneConnections;
import io.github.janguenter.bluemap.chipped.model.PillarAxis;
import io.github.janguenter.bluemap.chipped.model.PillarSelector;
import io.github.janguenter.bluemap.chipped.model.PillarTextureRole;
import io.github.janguenter.bluemap.chipped.profile.Chipped402Athena406Profile;
import io.github.janguenter.bluemap.chipped.profile.ChippedDefinition;

import java.util.function.Consumer;

/** Static structural renderer for the seven exact Chipped Athena loader families. */
final class ChippedRenderer implements BlockRenderer {

    private static final float PANE_MIN = 7F / 16F;
    private static final float PANE_MAX = 9F / 16F;
    private static final float CARPET_HEIGHT = 1F / 16F;

    private final ResourcePack resourcePack;
    private final ChippedRuntime runtime;
    private final ResourceModelRenderer stock;
    private final AthenaQuadEmitter emitter;
    private final BoundedDiagnostics diagnostics = new BoundedDiagnostics();

    ChippedRenderer(
            ResourcePack resourcePack,
            TextureGallery textureGallery,
            RenderSettings renderSettings,
            ChippedRuntime runtime
    ) {
        this.resourcePack = resourcePack;
        this.runtime = runtime;
        this.stock = new ResourceModelRenderer(resourcePack, textureGallery, renderSettings);
        this.emitter = new AthenaQuadEmitter(resourcePack, textureGallery, renderSettings);
    }

    @Override
    public void render(
            BlockNeighborhood block,
            Variant original,
            TileModelView target,
            Color mapColor
    ) {
        int start = target.getStart();
        Color initialMapColor = new Color().set(mapColor);
        if (!runtime.route().isActive()) {
            renderStock(block, target, mapColor);
            return;
        }
        ChippedDefinition definition = Chipped402Athena406Profile.DEFINITIONS.get(
                block.getBlockState().getId().getFormatted()
        );
        if (definition == null) {
            diagnostics.report("unknown-routed-block");
            renderStock(block, target, mapColor);
            return;
        }

        emitter.beginVariantColor();
        try {
            boolean rendered = switch (definition.family()) {
                case CTM -> renderCtmCube(definition, block, target, mapColor);
                case PILLAR -> renderPillar(definition, block, target, mapColor);
                case GIANT -> renderGiant(definition, block, target, mapColor);
                case PANE_CTM -> renderPaneCtm(definition, block, target, mapColor);
                case CARPET_CTM -> renderCarpet(definition, block, target, mapColor);
                case LIMITED_PILLAR -> renderLimitedPillar(
                        definition, block, target, mapColor
                );
                case PANE_PILLAR -> renderPanePillar(definition, block, target, mapColor);
            };
            if (!rendered) {
                diagnostics.report("resource-render-failed");
                resetAndRenderStock(block, target, start, mapColor, initialMapColor);
            } else {
                emitter.finishVariantColor(mapColor);
            }
        } catch (MaxCapacityReachedException exception) {
            throw exception;
        } catch (IllegalArgumentException exception) {
            diagnostics.report("malformed-persisted-state");
            resetAndRenderStock(block, target, start, mapColor, initialMapColor);
        } catch (RuntimeException exception) {
            diagnostics.report("contained-render-failure");
            resetAndRenderStock(block, target, start, mapColor, initialMapColor);
        }
    }

    private boolean renderCtmCube(
            ChippedDefinition definition,
            BlockNeighborhood block,
            TileModelView target,
            Color mapColor
    ) {
        for (CubeFace face : CubeFace.values()) {
            if (sameBlock(block, face.normal())) {
                continue;
            }
            if (!emitCtmFace(
                    definition, block, target, mapColor, face, 0F,
                    ctmConnections(block, face, ChippedRenderer::sameState), true
            )) {
                return false;
            }
        }
        return true;
    }

    private boolean renderPillar(
            ChippedDefinition definition,
            BlockNeighborhood block,
            TileModelView target,
            Color mapColor
    ) {
        PillarAxis axis = PillarAxis.parse(block.getBlockState().getProperties().get("axis"));
        boolean first = sameState(block, axis.first());
        boolean second = sameState(block, axis.second());
        PillarTextureRole sideRole = PillarSelector.select(first, second);
        for (CubeFace face : CubeFace.values()) {
            String role = axis.isCap(face) ? "particle" : sideRole.wireName();
            if (!emitFull(
                    definition, role, block, target, mapColor, face, 0F,
                    axis.uvRotation(face), true
            )) {
                return false;
            }
        }
        return true;
    }

    private boolean renderGiant(
            ChippedDefinition definition,
            BlockNeighborhood block,
            TileModelView target,
            Color mapColor
    ) {
        for (CubeFace face : CubeFace.values()) {
            String role = Integer.toString(GiantTextureSelector.select(
                    face, block.getX(), block.getY(), block.getZ()
            ));
            if (!emitFull(
                    definition, role, block, target, mapColor, face, 0F, 0, true
            )) {
                return false;
            }
        }
        return true;
    }

    private boolean renderLimitedPillar(
            ChippedDefinition definition,
            BlockNeighborhood block,
            TileModelView target,
            Color mapColor
    ) {
        boolean above = sameBlock(block, new CubeFace.Vec(0, 1, 0));
        boolean below = sameBlock(block, new CubeFace.Vec(0, -1, 0));
        PillarTextureRole sideRole = PillarSelector.select(above, below);
        for (CubeFace face : CubeFace.values()) {
            if (sameBlock(block, face.normal())) {
                continue;
            }
            String role = face == CubeFace.UP || face == CubeFace.DOWN
                    ? "particle" : sideRole.wireName();
            if (!emitFull(
                    definition, role, block, target, mapColor, face, 0F, 0, true
            )) {
                return false;
            }
        }
        return true;
    }

    private boolean renderCarpet(
            ChippedDefinition definition,
            BlockNeighborhood block,
            TileModelView target,
            Color mapColor
    ) {
        for (CubeFace face : new CubeFace[]{
                CubeFace.NORTH, CubeFace.SOUTH, CubeFace.WEST, CubeFace.EAST
        }) {
            if (!emitter.emit(
                    block, target, mapColor, face, 0F,
                    0F, 0F, 1F, CARPET_HEIGHT,
                    Key.parse(definition.texture("particle")), 0, true
            )) {
                return false;
            }
        }
        for (CubeFace face : new CubeFace[]{CubeFace.UP, CubeFace.DOWN}) {
            float depth = face == CubeFace.UP ? 15F / 16F : 1F / 16F;
            if (!emitCtmFace(
                    definition, block, target, mapColor, face, depth,
                    ctmConnections(block, face, ChippedRenderer::sameState), false
            )) {
                return false;
            }
        }
        return true;
    }

    private boolean renderPaneCtm(
            ChippedDefinition definition,
            BlockNeighborhood block,
            TileModelView target,
            Color mapColor
    ) {
        PaneConnections connections = PaneConnections.parse(
                block.getBlockState().getProperties()
        );
        if (!emitPaneCaps(definition, block, target, mapColor, connections)) {
            return false;
        }
        for (CubeFace face : new CubeFace[]{
                CubeFace.NORTH, CubeFace.SOUTH, CubeFace.WEST, CubeFace.EAST
        }) {
            CtmConnections ctm = ctmConnections(
                    block, face, (origin, offset) -> paneCompatible(origin, offset, face)
            );
            if (!emitPaneCtmSide(
                    definition, block, target, mapColor, face, connections, ctm
            )) {
                return false;
            }
        }
        return true;
    }

    private boolean renderPanePillar(
            ChippedDefinition definition,
            BlockNeighborhood block,
            TileModelView target,
            Color mapColor
    ) {
        PaneConnections connections = PaneConnections.parse(
                block.getBlockState().getProperties()
        );
        if (!emitPaneCaps(definition, block, target, mapColor, connections)) {
            return false;
        }
        for (CubeFace face : new CubeFace[]{
                CubeFace.NORTH, CubeFace.SOUTH, CubeFace.WEST, CubeFace.EAST
        }) {
            if (!emitPanePillarSide(
                    definition, block, target, mapColor, face, connections
            )) {
                return false;
            }
        }
        return true;
    }

    private boolean emitPaneCaps(
            ChippedDefinition definition,
            BlockNeighborhood block,
            TileModelView target,
            Color mapColor,
            PaneConnections connections
    ) {
        Key edge = Key.parse(definition.texture("particle"));
        for (CubeFace face : new CubeFace[]{CubeFace.UP, CubeFace.DOWN}) {
            if (sameState(block, face.normal())) {
                continue;
            }
            if (!emitter.emit(
                    block, target, mapColor, face, 0F,
                    PANE_MIN, PANE_MIN, PANE_MAX, PANE_MAX, edge, 0, false
            )) {
                return false;
            }
            boolean north = face == CubeFace.DOWN ? connections.south() : connections.north();
            boolean south = face == CubeFace.DOWN ? connections.north() : connections.south();
            if (north && !emitter.emit(
                    block, target, mapColor, face, 0F,
                    PANE_MIN, PANE_MAX, PANE_MAX, 1F, edge, 0, false
            )) {
                return false;
            }
            if (south && !emitter.emit(
                    block, target, mapColor, face, 0F,
                    PANE_MIN, 0F, PANE_MAX, PANE_MIN, edge, 0, false
            )) {
                return false;
            }
            if (connections.east() && !emitter.emit(
                    block, target, mapColor, face, 0F,
                    PANE_MAX, PANE_MIN, 1F, PANE_MAX, edge, 0, false
            )) {
                return false;
            }
            if (connections.west() && !emitter.emit(
                    block, target, mapColor, face, 0F,
                    0F, PANE_MIN, PANE_MIN, PANE_MAX, edge, 0, false
            )) {
                return false;
            }
        }
        return true;
    }

    private boolean emitPaneCtmSide(
            ChippedDefinition definition,
            BlockNeighborhood block,
            TileModelView target,
            Color mapColor,
            CubeFace face,
            PaneConnections connections,
            CtmConnections ctm
    ) {
        if (ctm.completelyConnected()) {
            return emitFull(
                    definition, "empty", block, target, mapColor,
                    face, PANE_MIN, 0, false
            );
        }
        boolean outward = connections.connected(face);
        boolean rightState = connections.connected(counterClockwise(face));
        boolean leftState = connections.connected(clockwise(face));
        Key particle = Key.parse(definition.texture("particle"));
        if (leftState && rightState) {
            float minimum = outward ? PANE_MIN : 0.5F;
            return emitPaneCtmQuadrant(
                    definition, block, target, mapColor, face, ctm,
                    0F, minimum, 1F - minimum, 1F
            );
        }
        float minimum = outward ? PANE_MAX : PANE_MIN;
        if (leftState) {
            return emitter.emit(
                    block, target, mapColor, face, PANE_MIN,
                    0F, 0F, 1F - minimum, 1F, particle, 0, false
            );
        }
        if (rightState) {
            return emitter.emit(
                    block, target, mapColor, face, PANE_MIN,
                    minimum, 0F, 1F, 1F, particle, 0, false
            );
        }
        return outward || sameBlock(block, face.normal()) || emitter.emit(
                block, target, mapColor, face, PANE_MIN,
                PANE_MIN, 0F, PANE_MAX, 1F, particle, 0, false
        );
    }

    private boolean emitPanePillarSide(
            ChippedDefinition definition,
            BlockNeighborhood block,
            TileModelView target,
            Color mapColor,
            CubeFace face,
            PaneConnections connections
    ) {
        boolean outward = connections.connected(face);
        boolean rightState = connections.connected(counterClockwise(face));
        boolean leftState = connections.connected(clockwise(face));
        Key particle = Key.parse(definition.texture("particle"));
        if (leftState && rightState) {
            float minimum = outward ? PANE_MIN : 0.5F;
            boolean above = paneCompatible(block, new CubeFace.Vec(0, 1, 0), face);
            boolean below = paneCompatible(block, new CubeFace.Vec(0, -1, 0), face);
            String role = PillarSelector.select(above, below).wireName();
            Key texture = Key.parse(definition.texture(role));
            return emitter.emit(
                    block, target, mapColor, face, PANE_MIN,
                    0F, 0F, minimum, 1F, texture, 0, false
            ) && emitter.emit(
                    block, target, mapColor, face, PANE_MIN,
                    1F - minimum, 0F, 1F, 1F, texture, 0, false
            );
        }
        float minimum = outward ? PANE_MAX : PANE_MIN;
        if (leftState) {
            return emitter.emit(
                    block, target, mapColor, face, PANE_MIN,
                    0F, 0F, 1F - minimum, 1F, particle, 0, false
            );
        }
        if (rightState) {
            return emitter.emit(
                    block, target, mapColor, face, PANE_MIN,
                    minimum, 0F, 1F, 1F, particle, 0, false
            );
        }
        return outward || sameBlock(block, face.normal()) || emitter.emit(
                block, target, mapColor, face, PANE_MIN,
                PANE_MIN, 0F, PANE_MAX, 1F, particle, 0, false
        );
    }

    private boolean emitPaneCtmQuadrant(
            ChippedDefinition definition,
            BlockNeighborhood block,
            TileModelView target,
            Color mapColor,
            CubeFace face,
            CtmConnections ctm,
            float leftStart,
            float leftEnd,
            float rightStart,
            float rightEnd
    ) {
        return emitQuarter(
                definition, block, target, mapColor, face, PANE_MIN,
                leftStart, 0.5F, leftEnd, 1F, ctm.quadrants().get(0), false
        ) && emitQuarter(
                definition, block, target, mapColor, face, PANE_MIN,
                rightStart, 0.5F, rightEnd, 1F, ctm.quadrants().get(1), false
        ) && emitQuarter(
                definition, block, target, mapColor, face, PANE_MIN,
                leftStart, 0F, leftEnd, 0.5F, ctm.quadrants().get(2), false
        ) && emitQuarter(
                definition, block, target, mapColor, face, PANE_MIN,
                rightStart, 0F, rightEnd, 0.5F, ctm.quadrants().get(3), false
        );
    }

    private boolean emitCtmFace(
            ChippedDefinition definition,
            BlockNeighborhood block,
            TileModelView target,
            Color mapColor,
            CubeFace face,
            float depth,
            CtmConnections connections,
            boolean cullable
    ) {
        if (connections.completelyConnected()) {
            return emitFull(
                    definition, "empty", block, target, mapColor,
                    face, depth, 0, cullable
            );
        }
        return emitQuarter(
                definition, block, target, mapColor, face, depth,
                0F, 0.5F, 0.5F, 1F, connections.quadrants().get(0), cullable
        ) && emitQuarter(
                definition, block, target, mapColor, face, depth,
                0.5F, 0.5F, 1F, 1F, connections.quadrants().get(1), cullable
        ) && emitQuarter(
                definition, block, target, mapColor, face, depth,
                0F, 0F, 0.5F, 0.5F, connections.quadrants().get(2), cullable
        ) && emitQuarter(
                definition, block, target, mapColor, face, depth,
                0.5F, 0F, 1F, 0.5F, connections.quadrants().get(3), cullable
        );
    }

    private boolean emitQuarter(
            ChippedDefinition definition,
            BlockNeighborhood block,
            TileModelView target,
            Color mapColor,
            CubeFace face,
            float depth,
            float left,
            float bottom,
            float right,
            float top,
            CtmTextureRole role,
            boolean cullable
    ) {
        return emitter.emit(
                block, target, mapColor, face, depth, left, bottom, right, top,
                Key.parse(definition.texture(role.wireName())), 0, cullable
        );
    }

    private boolean emitFull(
            ChippedDefinition definition,
            String role,
            BlockNeighborhood block,
            TileModelView target,
            Color mapColor,
            CubeFace face,
            float depth,
            int rotation,
            boolean cullable
    ) {
        return emitter.emit(
                block, target, mapColor, face, depth, 0F, 0F, 1F, 1F,
                Key.parse(definition.texture(role)), rotation, cullable
        );
    }

    private static CtmConnections ctmConnections(
            BlockNeighborhood block,
            CubeFace face,
            ConnectionPredicate predicate
    ) {
        CubeFace.Vec up = face.localUp();
        CubeFace.Vec down = face.localDown();
        CubeFace.Vec left = face.localLeft();
        CubeFace.Vec right = face.localRight();
        return new CtmConnections(
                predicate.connected(block, up),
                predicate.connected(block, down),
                predicate.connected(block, left),
                predicate.connected(block, right),
                predicate.connected(block, up.add(left)),
                predicate.connected(block, up.add(right)),
                predicate.connected(block, down.add(left)),
                predicate.connected(block, down.add(right))
        );
    }

    private static boolean paneCompatible(
            BlockNeighborhood block,
            CubeFace.Vec offset,
            CubeFace face
    ) {
        ExtendedBlock neighbor = block.getNeighborBlock(offset.x(), offset.y(), offset.z());
        if (!neighbor.getBlockState().getId().equals(block.getBlockState().getId())) {
            return false;
        }
        try {
            PaneConnections connections = PaneConnections.parse(
                    neighbor.getBlockState().getProperties()
            );
            return connections.connected(clockwise(face))
                    && connections.connected(counterClockwise(face));
        } catch (IllegalArgumentException exception) {
            return false;
        }
    }

    static CubeFace clockwise(CubeFace face) {
        return switch (face) {
            case NORTH -> CubeFace.EAST;
            case EAST -> CubeFace.SOUTH;
            case SOUTH -> CubeFace.WEST;
            case WEST -> CubeFace.NORTH;
            default -> throw new IllegalArgumentException("not a horizontal face");
        };
    }

    static CubeFace counterClockwise(CubeFace face) {
        return switch (face) {
            case NORTH -> CubeFace.WEST;
            case WEST -> CubeFace.SOUTH;
            case SOUTH -> CubeFace.EAST;
            case EAST -> CubeFace.NORTH;
            default -> throw new IllegalArgumentException("not a horizontal face");
        };
    }

    private static boolean sameState(BlockNeighborhood block, CubeFace.Vec offset) {
        return block.getNeighborBlock(offset.x(), offset.y(), offset.z())
                .getBlockState().equals(block.getBlockState());
    }

    private static boolean sameBlock(BlockNeighborhood block, CubeFace.Vec offset) {
        return block.getNeighborBlock(offset.x(), offset.y(), offset.z())
                .getBlockState().getId().equals(block.getBlockState().getId());
    }

    private void resetAndRenderStock(
            BlockNeighborhood block,
            TileModelView target,
            int start,
            Color mapColor,
            Color initialMapColor
    ) {
        target.getTileModel().reset(start);
        target.initialize(start);
        mapColor.set(initialMapColor);
        renderStock(block, target, mapColor);
    }

    private void renderStock(
            BlockNeighborhood block,
            TileModelView target,
            Color mapColor
    ) {
        de.bluecolored.bluemap.core.resources.pack.resourcepack.blockstate.BlockState state =
                resourcePack.getBlockStates().get(block.getBlockState().getId());
        if (state == null) {
            return;
        }
        forEachIsolatedVariant(
                state,
                block.getBlockState(),
                block.getX(), block.getY(), block.getZ(),
                target,
                variant -> stock.render(block, variant, target, mapColor)
        );
    }

    static void forEachIsolatedVariant(
            de.bluecolored.bluemap.core.resources.pack.resourcepack.blockstate.BlockState state,
            BlockState worldState,
            int x,
            int y,
            int z,
            TileModelView target,
            Consumer<Variant> renderer
    ) {
        state.forEach(worldState, x, y, z, variant -> {
            target.initialize();
            renderer.accept(variant);
        });
    }

    @FunctionalInterface
    private interface ConnectionPredicate {
        boolean connected(BlockNeighborhood block, CubeFace.Vec offset);
    }
}
