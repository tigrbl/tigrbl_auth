import { Country } from './types';

export const DEFAULT_COUNTRIES: Country[] = [
  { code: 'US', name: 'United States', dialCode: '+1', flag: '🇺🇸', isAllowed: true, costPerSms: 0.007 },
  { code: 'GB', name: 'United Kingdom', dialCode: '+44', flag: '🇬🇧', isAllowed: true, costPerSms: 0.015 },
  { code: 'DE', name: 'Germany', dialCode: '+49', flag: '🇩🇪', isAllowed: true, costPerSms: 0.045 },
  { code: 'JP', name: 'Japan', dialCode: '+81', flag: '🇯🇵', isAllowed: true, costPerSms: 0.052 },
  { code: 'AU', name: 'Australia', dialCode: '+61', flag: '🇦🇺', isAllowed: true, costPerSms: 0.038 },
  { code: 'BR', name: 'Brazil', dialCode: '+55', flag: '🇧🇷', isAllowed: true, costPerSms: 0.024 },
  { code: 'CH', name: 'Switzerland', dialCode: '+41', flag: '🇨🇭', isAllowed: true, costPerSms: 0.080 },
  { code: 'IN', name: 'India', dialCode: '+91', flag: '🇮🇳', isAllowed: true, costPerSms: 0.012 },
  { code: 'SO', name: 'Somalia (High Risk/Premium)', dialCode: '+252', flag: '🇸🇴', isAllowed: false, costPerSms: 0.350 },
  { code: 'KP', name: 'North Korea (Sanctioned)', dialCode: '+850', flag: '🇰🇵', isAllowed: false, costPerSms: 0.500 },
];
