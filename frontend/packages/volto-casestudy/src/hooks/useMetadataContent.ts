import { useEffect, useState } from 'react';

/**
 * Resolve the content a metadata block should render.
 *
 * With no `targetPath` the block describes the page it sits on, so the current
 * `properties` are used directly. With one, the referenced item is fetched
 * from the REST API.
 *
 * The fetch is client-only: during SSR there is no `window`, and the block
 * renders nothing rather than blocking the response.
 *
 * @param targetPath - Absolute URL of the referenced item, if any.
 * @param properties - The current page's content.
 * @returns The content to render, or `null` while it is not available yet.
 */
export function useMetadataContent<T>(
  targetPath: string | undefined,
  properties: T | undefined,
): T | null {
  const [externalContent, setExternalContent] = useState<T | null>(null);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  useEffect(() => {
    if (!isClient || !targetPath) {
      setExternalContent(null);
      return;
    }

    const relativePath = targetPath.replace(/^https?:\/\/[^/]+/, '');
    const targetUrl = `${window.location.origin}/++api++${relativePath}`;

    fetch(targetUrl, { headers: { Accept: 'application/json' } })
      .then((res) => (res.ok ? res.json() : null))
      .then((jsonData) => {
        if (jsonData) setExternalContent(jsonData as T);
      })
      .catch(() => {});
  }, [targetPath, isClient]);

  if (!isClient) return null;
  return targetPath ? externalContent : properties ?? null;
}

export default useMetadataContent;
