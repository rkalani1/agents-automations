import { safePath, SANDBOX_DIR, getValidNoteFiles } from './agent';
import * as path from 'path';
import * as fs from 'fs';

jest.mock('fs', () => {
  const actualFs = jest.requireActual('fs');
  return {
    ...actualFs,
    existsSync: jest.fn(),
    readdirSync: jest.fn(),
  };
});

describe('safePath', () => {
  it('should resolve paths inside the sandbox directory', () => {
    const validPath = 'notes/test.txt';
    const result = safePath(validPath);
    expect(result).toBe(path.resolve(SANDBOX_DIR, validPath));
  });

  it('should allow the sandbox directory itself', () => {
    const result = safePath('');
    expect(result).toBe(SANDBOX_DIR);
  });

  it('should throw an error for paths outside the sandbox', () => {
    const invalidPath = '../outside.txt';
    expect(() => safePath(invalidPath)).toThrow(
      `Path '${invalidPath}' resolves outside sandbox directory '${SANDBOX_DIR}'. Access denied.`
    );
  });

  it('should handle absolute paths that resolve inside the sandbox', () => {
    const absolutePath = path.resolve(SANDBOX_DIR, 'notes/test.txt');
    const result = safePath(absolutePath);
    expect(result).toBe(absolutePath);
  });

  it('should throw an error for absolute paths that resolve outside the sandbox', () => {
    const invalidAbsolutePath = path.resolve('/tmp/outside.txt');
    expect(() => safePath(invalidAbsolutePath)).toThrow();
  });

  it('should prevent directory traversal attacks', () => {
    const traversalPath = 'notes/../../outside.txt';
    expect(() => safePath(traversalPath)).toThrow();
  });
});

describe('getValidNoteFiles', () => {
  let exitSpy: jest.SpyInstance;
  let consoleErrorSpy: jest.SpyInstance;

  beforeEach(() => {
    exitSpy = jest.spyOn(process, 'exit').mockImplementation((() => {
      // Mock process.exit to throw an error so execution stops, simulating real exit
      throw new Error('process.exit called');
    }) as any);
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    (fs.existsSync as jest.Mock).mockReset();
    (fs.readdirSync as jest.Mock).mockReset();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('should exit and log error if the notes directory does not exist', () => {
    (fs.existsSync as jest.Mock).mockReturnValue(false);

    expect(() => {
      getValidNoteFiles('nonexistent/dir');
    }).toThrow('process.exit called');

    expect(fs.existsSync).toHaveBeenCalledWith('nonexistent/dir');
    expect(consoleErrorSpy).toHaveBeenCalledWith('ERROR: Sandbox notes directory not found: nonexistent/dir');
    expect(exitSpy).toHaveBeenCalledWith(1);
  });

  it('should exit and log error if no valid .txt or .md files are found', () => {
    (fs.existsSync as jest.Mock).mockReturnValue(true);
    (fs.readdirSync as jest.Mock).mockReturnValue(['test.json', 'test.csv', 'test', 'not_a_note.jpg']);

    expect(() => {
      getValidNoteFiles('empty/dir');
    }).toThrow('process.exit called');

    expect(fs.existsSync).toHaveBeenCalledWith('empty/dir');
    expect(fs.readdirSync).toHaveBeenCalledWith('empty/dir');
    expect(consoleErrorSpy).toHaveBeenCalledWith('ERROR: No .txt or .md files found in ./sandbox/notes/');
    expect(exitSpy).toHaveBeenCalledWith(1);
  });

  it('should return valid .txt and .md files', () => {
    (fs.existsSync as jest.Mock).mockReturnValue(true);
    (fs.readdirSync as jest.Mock).mockReturnValue(['test.txt', 'test.md', 'test.json']);

    const result = getValidNoteFiles('valid/dir');

    expect(fs.existsSync).toHaveBeenCalledWith('valid/dir');
    expect(fs.readdirSync).toHaveBeenCalledWith('valid/dir');
    expect(result).toEqual(['test.txt', 'test.md']);
    expect(exitSpy).not.toHaveBeenCalled();
    expect(consoleErrorSpy).not.toHaveBeenCalled();
  });

  it('should limit returned files to 50', () => {
    (fs.existsSync as jest.Mock).mockReturnValue(true);
    const manyFiles = Array(60).fill('test.txt');
    (fs.readdirSync as jest.Mock).mockReturnValue(manyFiles);

    const result = getValidNoteFiles('large/dir');

    expect(fs.existsSync).toHaveBeenCalledWith('large/dir');
    expect(fs.readdirSync).toHaveBeenCalledWith('large/dir');
    expect(result.length).toBe(50);
    expect(exitSpy).not.toHaveBeenCalled();
    expect(consoleErrorSpy).not.toHaveBeenCalled();
  });
});
