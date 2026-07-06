import { safePath, SANDBOX_DIR } from './agent';
import * as path from 'path';

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

  it('should prevent symlink traversal attacks', () => {
    const fs = require('fs');
    // Create a sandbox dir and a file outside it for testing
    fs.mkdirSync('./sandbox', { recursive: true });
    fs.mkdirSync('./outside', { recursive: true });
    fs.writeFileSync('./outside/secret.txt', 'secret');

    // Create a symlink inside sandbox pointing outside
    try {
      fs.symlinkSync('../outside', './sandbox/link');
    } catch (e: any) {
      if (e.code !== 'EEXIST') throw e;
    }

    const symlinkPath = 'link/secret.txt';
    expect(() => safePath(symlinkPath)).toThrow();

    const newSymlinkPath = 'link/new_secret.txt';
    expect(() => safePath(newSymlinkPath)).toThrow();
  });
});
