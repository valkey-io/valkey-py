"""
Binary preservation tests for search results.

These tests are in a separate file because the main search test suite (test_search.py)
has compatibility issues with the current Valkey search module version. Most existing
search tests fail due to unsupported field types and parameters (e.g., TEXT fields,
SKIPINITIALSCAN, etc.).

Our binary preservation functionality works correctly with the current search module
using direct FT.CREATE commands and KNN vector queries, so we maintain these tests
separately to ensure the feature remains properly tested while the broader search
test compatibility issues are resolved.
"""

import struct

import pytest
import valkey

from .conftest import _get_client, is_resp2_connection, skip_ifmodversion_lt


@pytest.mark.valkeymod
@skip_ifmodversion_lt("1.0.0", "search")
def test_vector_binary_preservation_default_behavior(request):
    """Test that default behavior still corrupts binary data (backward compatibility)"""
    client = _get_client(valkey.Valkey, request, decode_responses=False)

    # Create index with vector field using direct command
    client.execute_command(
        "FT.CREATE", "test_idx", "SCHEMA",
        "embedding", "VECTOR", "FLAT", "6", "TYPE", "FLOAT32", "DIM", "3",
        "DISTANCE_METRIC", "COSINE"
    )

    # Create vector data as bytes (simulating embeddings)
    vec1 = [0.1, 0.2, 0.3]
    vec1_bytes = struct.pack('3f', *vec1)

    # Store document with vector
    client.hset("doc:1", mapping={"embedding": vec1_bytes})

    # Search without preserve_bytes (default behavior) using KNN query
    results = client.ft("test_idx").search(
        "*=>[KNN 1 @embedding $vec]", {"vec": vec1_bytes}
    )

    if is_resp2_connection(client):
        doc = results.docs[0]
        # Default behavior should decode bytes to string (corrupting binary data)
        assert isinstance(doc.embedding, str)
        assert doc.embedding != vec1_bytes  # Should be corrupted

    client.execute_command("FT.DROPINDEX", "test_idx")


@pytest.mark.valkeymod
@skip_ifmodversion_lt("1.0.0", "search")
def test_vector_binary_preservation_enabled(request):
    """Test that preserve_bytes=True preserves binary vector data"""
    client = _get_client(valkey.Valkey, request, decode_responses=False)

    # Create index with vector field using direct command
    client.execute_command(
        "FT.CREATE", "test_idx", "SCHEMA",
        "embedding", "VECTOR", "FLAT", "6", "TYPE", "FLOAT32", "DIM", "3",
        "DISTANCE_METRIC", "COSINE"
    )

    # Create vector data as bytes (simulating embeddings)
    vec1 = [0.1, 0.2, 0.3]
    vec1_bytes = struct.pack('3f', *vec1)

    # Store document with vector
    client.hset("doc:1", mapping={"embedding": vec1_bytes})

    # Search with preserve_bytes=True using KNN query
    results = client.ft("test_idx").search(
        "*=>[KNN 1 @embedding $vec]", {"vec": vec1_bytes}, preserve_bytes=True
    )

    if is_resp2_connection(client):
        doc = results.docs[0]
        # With preserve_bytes=True, binary data should be preserved
        assert isinstance(doc.embedding, bytes)
        assert doc.embedding == vec1_bytes

    client.execute_command("FT.DROPINDEX", "test_idx")


@pytest.mark.valkeymod
@skip_ifmodversion_lt("1.0.0", "search")
def test_multiple_field_types_and_vectors(request):
    """Test binary preservation with multiple field types and vector dimensions"""
    client = _get_client(valkey.Valkey, request, decode_responses=False)

    # Create index with diverse field types and different vector dimensions
    client.execute_command(
        "FT.CREATE", "test_idx", "SCHEMA",
        "title", "TAG",
        "price", "NUMERIC",
        "embedding_3d", "VECTOR", "FLAT", "6", "TYPE", "FLOAT32", "DIM", "3",
        "DISTANCE_METRIC", "COSINE",
        "embedding_4d", "VECTOR", "FLAT", "6", "TYPE", "FLOAT32", "DIM", "4",
        "DISTANCE_METRIC", "L2",
        "binary_data", "TAG"
    )

    # Create test data with different vector dimensions
    vec_3d = [0.1, 0.2, 0.3]
    vec_3d_bytes = struct.pack("3f", *vec_3d)
    vec_4d = [0.4, 0.5, 0.6, 0.7]
    vec_4d_bytes = struct.pack("4f", *vec_4d)

    # Store multiple documents
    for i in range(3):
        client.hset(f"doc:{i + 1}", mapping={
            "title": f"item_{i + 1}",
            "price": 10.0 + i,
            "embedding_3d": vec_3d_bytes,
            "embedding_4d": vec_4d_bytes,
            "binary_data": b"binary_content"
        })

    # Test with multiple results (KNN 3 instead of KNN 1)
    results = client.ft("test_idx").search(
        "*=>[KNN 3 @embedding_3d $vec]",
        {"vec": vec_3d_bytes},
        preserve_bytes=True,
        binary_fields=["embedding_3d", "embedding_4d"]
    )

    if is_resp2_connection(client):
        assert len(results.docs) == 3
        for doc in results.docs:
            # Vector fields should be preserved as bytes
            assert isinstance(doc.embedding_3d, bytes)
            assert doc.embedding_3d == vec_3d_bytes
            assert isinstance(doc.embedding_4d, bytes)
            assert doc.embedding_4d == vec_4d_bytes
            # Non-binary fields should be strings
            assert isinstance(doc.title, str)
            assert isinstance(doc.binary_data, str)

    client.execute_command("FT.DROPINDEX", "test_idx")


@pytest.mark.valkeymod
@skip_ifmodversion_lt("1.0.0", "search")
def test_binary_fields_selective_preservation(request):
    """Test that binary_fields parameter selectively preserves specific fields"""
    client = _get_client(valkey.Valkey, request, decode_responses=False)

    # Create index with vector and tag fields using direct command
    client.execute_command(
        "FT.CREATE", "test_idx", "SCHEMA",
        "embedding1", "VECTOR", "FLAT", "6", "TYPE", "FLOAT32", "DIM", "3",
        "DISTANCE_METRIC", "COSINE",
        "embedding2", "VECTOR", "FLAT", "6", "TYPE", "FLOAT32", "DIM", "3",
        "DISTANCE_METRIC", "COSINE",
        "binary_tag", "TAG"
    )

    # Create vector data as bytes
    vec1 = [0.1, 0.2, 0.3]
    vec1_bytes = struct.pack("3f", *vec1)
    vec2 = [0.4, 0.5, 0.6]
    vec2_bytes = struct.pack("3f", *vec2)

    # Store document with vectors and tag
    client.hset("doc:1", mapping={
        "embedding1": vec1_bytes,
        "embedding2": vec2_bytes,
        "binary_tag": b"test_tag"
    })

    # Search with selective binary preservation (only embedding1) using KNN query
    results = client.ft("test_idx").search(
        "*=>[KNN 1 @embedding1 $vec]",
        {"vec": vec1_bytes},
        preserve_bytes=True,
        binary_fields=["embedding1"]
    )

    if is_resp2_connection(client):
        doc = results.docs[0]
        assert isinstance(doc.embedding1, bytes)
        assert doc.embedding1 == vec1_bytes
        assert isinstance(doc.embedding2, str)
        assert isinstance(doc.binary_tag, str)

    client.execute_command("FT.DROPINDEX", "test_idx")
