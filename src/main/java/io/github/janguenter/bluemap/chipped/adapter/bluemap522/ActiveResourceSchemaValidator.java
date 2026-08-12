/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chipped.adapter.bluemap522;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import de.bluecolored.bluemap.core.resources.pack.resourcepack.ResourcePack;
import io.github.janguenter.bluemap.chipped.profile.ChippedDefinition;
import io.github.janguenter.bluemap.chipped.profile.LoaderFamily;

import java.io.IOException;
import java.io.StringReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HashMap;
import java.util.HexFormat;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

/** Validates the active installed JSON schema without retaining third-party bytes. */
final class ActiveResourceSchemaValidator {

    private static final int MAX_JSON_BYTES = 128 * 1024;

    private ActiveResourceSchemaValidator() {
    }

    static Result validate(
            ResourcePack resourcePack,
            Iterable<Path> roots,
            Map<String, ChippedDefinition> definitions
    ) throws IOException, InterruptedException {
        Map<String, String> blockPaths = new LinkedHashMap<>();
        Map<String, String> modelPaths = new LinkedHashMap<>();
        for (ChippedDefinition definition : definitions.values()) {
            blockPaths.put(blockstatePath(definition.blockId()), definition.blockId());
            modelPaths.put(modelPath(definition.modelId()), definition.blockId());
        }

        Map<String, byte[]> activeBlockstates = new HashMap<>();
        Map<String, byte[]> activeModels = new HashMap<>();
        for (Path root : roots) {
            if (Thread.interrupted()) {
                throw new InterruptedException();
            }
            resourcePack.loadResourcePath(root, activeRoot -> {
                collect(activeRoot, blockPaths, activeBlockstates);
                collect(activeRoot, modelPaths, activeModels);
            });
        }
        if (activeBlockstates.size() != definitions.size()) {
            return Result.invalid("active-blockstate-roster-mismatch");
        }
        if (activeModels.size() != definitions.size()) {
            return Result.invalid("active-model-roster-mismatch");
        }

        for (ChippedDefinition definition : definitions.values()) {
            byte[] blockstate = activeBlockstates.get(definition.blockId());
            byte[] model = activeModels.get(definition.blockId());
            if (!validBlockstate(blockstate, definition)) {
                return Result.invalid("active-blockstate-schema-mismatch");
            }
            if (!validModel(model, definition)) {
                return Result.invalid("active-model-schema-mismatch");
            }
        }
        return Result.success();
    }

    private static void collect(
            Path root,
            Map<String, String> requested,
            Map<String, byte[]> output
    ) throws IOException {
        for (Map.Entry<String, String> entry : requested.entrySet()) {
            if (output.containsKey(entry.getValue())) {
                continue;
            }
            Path resource = root.resolve(entry.getKey());
            if (!Files.isRegularFile(resource)) {
                continue;
            }
            long size = Files.size(resource);
            if (size < 1 || size > MAX_JSON_BYTES) {
                output.put(entry.getValue(), new byte[0]);
                continue;
            }
            byte[] raw = Files.readAllBytes(resource);
            output.put(entry.getValue(), raw.length <= MAX_JSON_BYTES ? raw : new byte[0]);
        }
    }

    private static boolean validBlockstate(byte[] raw, ChippedDefinition definition) {
        JsonObject root = parseObject(raw);
        if (root == null) {
            return false;
        }
        Set<String> expectedKeys = definition.family() == LoaderFamily.GIANT
                ? Set.of("athena:loader", "ctm_textures", "height", "variants", "width")
                : Set.of("athena:loader", "ctm_textures", "variants");
        if (!root.keySet().equals(expectedKeys)
                || !stringValue(root.get("athena:loader")).equals(
                        "athena:" + definition.family().wireName()
                )) {
            return false;
        }
        if (definition.family() == LoaderFamily.GIANT
                && (integerValue(root.get("width")) != 2
                || integerValue(root.get("height")) != 2)) {
            return false;
        }

        JsonObject variants = objectValue(root.get("variants"));
        if (variants == null || !variants.keySet().equals(Set.of(""))) {
            return false;
        }
        JsonObject variant = objectValue(variants.get(""));
        if (variant == null || !variant.keySet().equals(Set.of("model"))
                || !definition.modelId().equals(stringValue(variant.get("model")))) {
            return false;
        }

        JsonObject textures = objectValue(root.get("ctm_textures"));
        if (textures == null
                || !textures.keySet().equals(Set.copyOf(definition.family().textureRoles()))) {
            return false;
        }
        for (String role : definition.family().textureRoles()) {
            if (!definition.texture(role).equals(stringValue(textures.get(role)))) {
                return false;
            }
        }
        return true;
    }

    private static boolean validModel(byte[] raw, ChippedDefinition definition) {
        JsonObject root = parseObject(raw);
        if (root == null || !root.keySet().equals(Set.of("parent", "textures"))
                || !definition.modelParent().equals(stringValue(root.get("parent")))) {
            return false;
        }
        JsonObject textures = objectValue(root.get("textures"));
        if (textures == null || textures.size() == 0) {
            return false;
        }
        TreeMap<String, String> values = new TreeMap<>();
        for (Map.Entry<String, JsonElement> entry : textures.entrySet()) {
            String value = stringValue(entry.getValue());
            if (value.isEmpty()) {
                return false;
            }
            values.put(entry.getKey(), value);
        }
        StringBuilder canonical = new StringBuilder();
        values.forEach((key, value) -> canonical.append(key).append('=').append(value).append('\n'));
        return definition.modelTextureMapSha256().equals(
                sha256(canonical.toString().getBytes(StandardCharsets.UTF_8))
        );
    }

    private static JsonObject parseObject(byte[] raw) {
        if (raw == null || raw.length == 0 || raw.length > MAX_JSON_BYTES) {
            return null;
        }
        try {
            JsonElement value = JsonParser.parseReader(
                    new StringReader(new String(raw, StandardCharsets.UTF_8))
            );
            return value.isJsonObject() ? value.getAsJsonObject() : null;
        } catch (RuntimeException exception) {
            return null;
        }
    }

    private static JsonObject objectValue(JsonElement value) {
        return value != null && value.isJsonObject() ? value.getAsJsonObject() : null;
    }

    private static String stringValue(JsonElement value) {
        try {
            return value != null && value.isJsonPrimitive() && value.getAsJsonPrimitive().isString()
                    ? value.getAsString() : "";
        } catch (RuntimeException exception) {
            return "";
        }
    }

    private static int integerValue(JsonElement value) {
        try {
            return value != null && value.isJsonPrimitive()
                    ? value.getAsInt() : Integer.MIN_VALUE;
        } catch (RuntimeException exception) {
            return Integer.MIN_VALUE;
        }
    }

    private static String blockstatePath(String blockId) {
        return "assets/chipped/blockstates/" + blockId.substring("chipped:".length()) + ".json";
    }

    private static String modelPath(String modelId) {
        int separator = modelId.indexOf(':');
        String namespace = separator < 0 ? "minecraft" : modelId.substring(0, separator);
        String value = separator < 0 ? modelId : modelId.substring(separator + 1);
        return "assets/" + namespace + "/models/" + value + ".json";
    }

    private static String sha256(byte[] raw) {
        try {
            return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(raw));
        } catch (NoSuchAlgorithmException exception) {
            throw new IllegalStateException("SHA-256 unavailable", exception);
        }
    }

    record Result(boolean valid, String reason) {

        private static Result success() {
            return new Result(true, "exact-active-schema");
        }

        private static Result invalid(String reason) {
            return new Result(false, reason);
        }
    }
}
