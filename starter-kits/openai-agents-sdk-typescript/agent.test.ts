import { safePath, SANDBOX_DIR, readNotes } from './agent';
import * as path from 'path';
import * as fs from 'fs';

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

describe('readNotes', () => {
  const testDir = path.join(SANDBOX_DIR, 'test_notes');
  const testFile = path.join(testDir, 'test.txt');

  beforeAll(() => {
    if (!fs.existsSync(SANDBOX_DIR)) {
      fs.mkdirSync(SANDBOX_DIR, { recursive: true });
    }
    if (!fs.existsSync(testDir)) {
      fs.mkdirSync(testDir, { recursive: true });
    }
  });

  afterAll(() => {
    if (fs.existsSync(testDir)) {
      fs.rmSync(testDir, { recursive: true, force: true });
    }
  });

  it('should read a valid file', () => {
    const content = 'This is a test note.';
    fs.writeFileSync(testFile, content, 'utf-8');

    const result = readNotes('test_notes/test.txt');
    expect(result).toBe(content);
  });

  it('should throw an error if the file does not exist', () => {
    expect(() => readNotes('test_notes/nonexistent.txt')).toThrow(
      'File not found in sandbox: test_notes/nonexistent.txt'
    );
  });

  it('should throw an error if the path is not a file', () => {
    expect(() => readNotes('test_notes')).toThrow(
      'Path is not a file: test_notes'
    );
  });
});
