
import { useState, useEffect, useCallback } from 'react';
import { PlatformConfig } from '../types';
import { DEFAULT_PLATFORM_CONFIG } from '../defaults';

export const usePlatform = () => {
  const [platform, setPlatform] = useState<PlatformConfig>(() => {
    const config: any = {};
    const keys = Object.keys(DEFAULT_PLATFORM_CONFIG) as (keyof PlatformConfig)[];

    const parseStoredValue = (key: keyof PlatformConfig, value: string | null) => {
      if (value === null) return undefined;
      if (key === 'enableBrandingSettings' || key === 'enableAdapterSettings') {
        return value.toLowerCase() === 'true';
      }
      return value;
    };

    keys.forEach(key => {
      // Priority: LocalStorage (Runtime Overrides) > defaults.ts (Env or Static)
      const storedValue = parseStoredValue(key, localStorage.getItem(`tigrbl_auth_platform_${key}`));
      config[key] = storedValue !== undefined ? storedValue : DEFAULT_PLATFORM_CONFIG[key];
    });

    return config as PlatformConfig;
  });

  const applyBranding = useCallback((config: PlatformConfig) => {
    const root = document.documentElement;

    // Core Colors
    root.style.setProperty('--brand-primary', config.primaryColor);
    root.style.setProperty('--brand-secondary', config.secondaryColor);
    root.style.setProperty('--bg-app', config.backgroundColor);

    // Border Radius
    root.style.setProperty('--radius-ui', config.borderRadius);

    const hexToRgb = (hex: string) => {
      const cleanHex = hex.replace('#', '');
      const r = parseInt(cleanHex.substring(0, 2), 16);
      const g = parseInt(cleanHex.substring(2, 4), 16);
      const b = parseInt(cleanHex.substring(4, 6), 16);
      return `${r}, ${g}, ${b}`;
    };

    root.style.setProperty('--brand-primary-rgb', hexToRgb(config.primaryColor));
    root.style.setProperty('--brand-secondary-rgb', hexToRgb(config.secondaryColor));
  }, []);

  const updateMetadata = useCallback((config: PlatformConfig) => {
    const setMetaTag = (attribute: 'name' | 'property', key: string, content: string) => {
      if (!content) return;
      let tag = document.querySelector(`meta[${attribute}="${key}"]`) as HTMLMetaElement | null;
      if (!tag) {
        tag = document.createElement('meta');
        tag.setAttribute(attribute, key);
        document.head.appendChild(tag);
      }
      tag.setAttribute('content', content);
    };

    const setLinkTag = (rel: string, href: string) => {
      if (!href) return;
      let tag = document.querySelector(`link[rel="${rel}"]`) as HTMLLinkElement | null;
      if (!tag) {
        tag = document.createElement('link');
        tag.setAttribute('rel', rel);
        document.head.appendChild(tag);
      }
      tag.setAttribute('href', href);
    };

    const title = config.embedTitle || config.name;
    document.title = title;

    const description = config.embedDescription;
    const image = config.embedImage;
    const url = config.embedUrl || window.location.origin;

    setMetaTag('name', 'description', description);
    setMetaTag('property', 'og:title', title);
    setMetaTag('property', 'og:description', description);
    setMetaTag('property', 'og:image', image);
    setMetaTag('property', 'og:url', url);
    setMetaTag('property', 'og:type', 'website');

    setMetaTag('name', 'twitter:card', image ? 'summary_large_image' : 'summary');
    setMetaTag('name', 'twitter:title', title);
    setMetaTag('name', 'twitter:description', description);
    if (image) setMetaTag('name', 'twitter:image', image);

    setLinkTag('canonical', url);
  }, []);

  useEffect(() => {
    applyBranding(platform);
    updateMetadata(platform);
  }, [platform, applyBranding, updateMetadata]);

  const updatePlatform = useCallback((updates: Partial<PlatformConfig>) => {
    setPlatform(prev => {
      const next = { ...prev, ...updates };
      Object.entries(updates).forEach(([key, val]) => {
        if (val !== undefined) {
          const serialized = typeof val === 'boolean' ? String(val) : String(val);
          localStorage.setItem(`tigrbl_auth_platform_${key}`, serialized);
        }
      });
      return next;
    });
  }, []);

  return { ...platform, updatePlatform };
};
