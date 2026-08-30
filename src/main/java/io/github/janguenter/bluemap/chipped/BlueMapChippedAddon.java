/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chipped;

import de.bluecolored.bluemap.core.BlueMap;
import io.github.janguenter.bluemap.addon.adapter.api.bluemap523.BlueMapRuntimeCompatibility;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

/** BlueMap add-on entrypoint installed before resource-pack construction. */
public final class BlueMapChippedAddon implements Runnable {

    public BlueMapChippedAddon() {
    }

    @Override
    public void run() {
        try {
            if (!runtimeSupported(BlueMap.VERSION, BlueMap.GIT_HASH)) {
                inactive("unsupported BlueMap internal ABI", null);
                return;
            }
            Class<?> adapter = loadAdapter(true);
            Method install = adapter.getMethod("install");
            install.invoke(null);
        } catch (InvocationTargetException exception) {
            inactive("exact adapter initialization failed", exception.getCause());
        } catch (ReflectiveOperationException | LinkageError | RuntimeException exception) {
            inactive("exact adapter is unavailable", exception);
        }
    }

    static boolean runtimeSupported(String version, String gitHash) {
        return BlueMapRuntimeCompatibility.matches(
                version,
                gitHash
        );
    }

    static Class<?> loadAdapter(boolean initialize) throws ClassNotFoundException {
        return Class.forName(
                "io.github.janguenter.bluemap.chipped.adapter.bluemap523.BlueMap523Adapter",
                initialize,
                BlueMapChippedAddon.class.getClassLoader()
        );
    }

    private static void inactive(String reason, Throwable cause) {
        String detail = cause == null ? "" : " (" + cause.getClass().getSimpleName() + ")";
        System.err.println("BlueMap Chipped add-on is inactive: " + reason + detail + ".");
    }
}
