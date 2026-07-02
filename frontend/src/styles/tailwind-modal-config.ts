/**
 * CUSTOMIZAÇÕES TAILWIND PARA O MODAL
 * 
 * Adicione estas configurações ao seu tailwind.config.ts para melhorar
 * o design e adicionar efeitos especiais ao modal.
 * 
 * Exemplo de como adicionar ao tailwind.config.ts:
 * 
 * export default {
 *   theme: {
 *     extend: {
 *       animations: { ... },
 *       keyframes: { ... },
 *       boxShadow: { ... },
 *       // etc
 *     }
 *   }
 * }
 */

// ╔════════════════════════════════════════════════════════════════╗
// ║              ANIMAÇÕES E TRANSIÇÕES                            ║
// ╚════════════════════════════════════════════════════════════════╝

export const tailwindAnimations = {
  animation: {
    'fade-in': 'fadeIn 0.3s ease-in-out',
    'slide-up': 'slideUp 0.3s ease-out',
    'slide-down': 'slideDown 0.3s ease-out',
    'scale-in': 'scaleIn 0.2s ease-out',
    'pulse-subtle': 'pulseSubtle 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
    'badge-pop': 'badgePop 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55)',
  },
  keyframes: {
    fadeIn: {
      '0%': { opacity: '0' },
      '100%': { opacity: '1' },
    },
    slideUp: {
      '0%': {
        opacity: '0',
        transform: 'translateY(10px)',
      },
      '100%': {
        opacity: '1',
        transform: 'translateY(0)',
      },
    },
    slideDown: {
      '0%': {
        opacity: '0',
        transform: 'translateY(-10px)',
      },
      '100%': {
        opacity: '1',
        transform: 'translateY(0)',
      },
    },
    scaleIn: {
      '0%': {
        opacity: '0',
        transform: 'scale(0.95)',
      },
      '100%': {
        opacity: '1',
        transform: 'scale(1)',
      },
    },
    pulseSubtle: {
      '0%, 100%': { opacity: '1' },
      '50%': { opacity: '0.8' },
    },
    badgePop: {
      '0%': {
        opacity: '0',
        transform: 'scale(0.3) rotate(-45deg)',
      },
      '50%': {
        transform: 'scale(1.1) rotate(0deg)',
      },
      '100%': {
        opacity: '1',
        transform: 'scale(1) rotate(0deg)',
      },
    },
  },
}

// ╔════════════════════════════════════════════════════════════════╗
// ║              SOMBRAS ESPECIAIS                                 ║
// ╚════════════════════════════════════════════════════════════════╝

export const tailwindBoxShadows = {
  boxShadow: {
    'modal': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    'modal-lg': '0 25px 100px -12px rgba(0, 0, 0, 0.35)',
    'elevation-1': '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
    'elevation-2': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    'elevation-3': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    'elevation-4': '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
    'card-hover': '0 20px 25px -5px rgba(0, 0, 0, 0.15)',
    'inset-light': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.05)',
  },
}

// ╔════════════════════════════════════════════════════════════════╗
// ║              CORES ESTENDIDAS                                  ║
// ╚════════════════════════════════════════════════════════════════╝

export const tailwindColors = {
  colors: {
    // Cores corporativas personalizadas
    'telemetry': {
      50: '#f0f9ff',
      100: '#e0f2fe',
      200: '#bae6fd',
      300: '#7dd3fc',
      400: '#38bdf8',
      500: '#0ea5e9', // Primary
      600: '#0284c7',
      700: '#0369a1',
      800: '#075985',
      900: '#0c3d66',
    },
    'status': {
      'error': '#ef4444',
      'warning': '#f59e0b',
      'success': '#10b981',
      'info': '#3b82f6',
    },
  },
}

// ╔════════════════════════════════════════════════════════════════╗
// ║              GRADIENTES ÚTEIS                                  ║
// ╚════════════════════════════════════════════════════════════════╝

export const tailwindGradients = {
  backgroundImage: {
    'gradient-telemetry': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'gradient-success': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    'gradient-warning': 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
    'gradient-error': 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
    'gradient-modal-header': 'linear-gradient(to right, #0ea5e9 0%, #06b6d4 100%)',
    'gradient-badge': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  },
}

// ╔════════════════════════════════════════════════════════════════╗
// ║              UTILIDADES CSS                                    ║
// ╚════════════════════════════════════════════════════════════════╝

export const tailwindUtilities = {
  utilities: {
    '.scrollbar-hide': {
      /* Firefox */
      'scrollbar-width': 'none',
      /* Safari and Chrome */
      '&::-webkit-scrollbar': {
        display: 'none',
      },
    },
    '.scrollbar-thin': {
      '&::-webkit-scrollbar': {
        width: '6px',
      },
      '&::-webkit-scrollbar-track': {
        'background': 'transparent',
      },
      '&::-webkit-scrollbar-thumb': {
        'background': '#cbd5e1',
        'border-radius': '3px',
      },
      '&::-webkit-scrollbar-thumb:hover': {
        'background': '#94a3b8',
      },
    },
    '.modal-backdrop': {
      'animation': 'fadeIn 0.3s ease-in-out',
    },
    '.modal-content': {
      'animation': 'scaleIn 0.3s ease-out',
    },
    '.tab-active': {
      'border-bottom-color': '#0ea5e9',
      'color': '#0284c7',
      'background-color': 'rgba(14, 165, 233, 0.05)',
    },
    '.editable-field-hover': {
      'transition': 'all 0.2s ease-out',
      '&:hover': {
        'background-color': '#f3f4f6',
      },
    },
    '.badge-status': {
      'display': 'inline-block',
      'padding': '0.375rem 0.75rem',
      'border-radius': '0.375rem',
      'font-size': '0.875rem',
      'font-weight': '600',
      'border-width': '1px',
    },
  },
}

// ╔════════════════════════════════════════════════════════════════╗
// ║              EXEMPLO COMPLETO PARA TAILWIND CONFIG             ║
// ╚════════════════════════════════════════════════════════════════╝

export const tailwindConfigExample = `
import type { Config } from 'tailwindcss'

export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
      },
      boxShadow: {
        'modal': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        'elevation-4': '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
      },
      colors: {
        telemetry: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          600: '#0284c7',
        },
      },
      backgroundImage: {
        'gradient-modal': 'linear-gradient(to right, #0ea5e9 0%, #06b6d4 100%)',
      },
    },
  },
  darkMode: 'class',
  plugins: [],
} satisfies Config
`
