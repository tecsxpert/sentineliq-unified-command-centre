package com.internship.tool.service;

import com.internship.tool.entity.User;
import com.internship.tool.exception.InvalidInputException;
import com.internship.tool.exception.ResourceNotFoundException;
import com.internship.tool.repository.UserRepository;
import org.junit.jupiter.api.*;
import org.mockito.*;
import org.springframework.data.domain.*;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class UserServiceTest {

    @Mock
    private UserRepository repo;

    @InjectMocks
    private UserService service;

    @Mock
    private EmailService emailService;

    @BeforeEach
    void setup() {
        MockitoAnnotations.openMocks(this);
    }

    //  1. Happy path: create user
    @Test
    void testCreateUserSuccess() {
        User user = new User(null, "Akhila", "a@test.com", "1234", null, null);

        when(repo.save(any(User.class))).thenReturn(user);

        User result = service.createUser(user);

        assertEquals("Akhila", result.getName());
        verify(repo, times(1)).save(user);
    }

    // 2. Name missing
    @Test
    void testCreateUserNameMissing() {
        User user = new User(null, "", "a@test.com", "1234", null, null);

        assertThrows(InvalidInputException.class, () -> service.createUser(user));
    }

    //  3. Email missing
    @Test
    void testCreateUserEmailMissing() {
        User user = new User(null, "Akhila", "", "1234", null, null);

        assertThrows(InvalidInputException.class, () -> service.createUser(user));
    }

    // 4. Password missing
    @Test
    void testCreateUserPasswordMissing() {
        User user = new User(null, "Akhila", "a@test.com", "", null, null);

        assertThrows(InvalidInputException.class, () -> service.createUser(user));
    }

    //  5. Get user by ID success
    @Test
    void testGetUserByIdSuccess() {
        User user = new User(1L, "Akhila", "a@test.com", "1234", null, null);

        when(repo.findById(1L)).thenReturn(Optional.of(user));

        User result = service.getUserById(1L);

        assertEquals(1L, result.getId());
    }

    //  6. Get user not found
    @Test
    void testGetUserByIdNotFound() {
        when(repo.findById(1L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> service.getUserById(1L));
    }

    //  7. Get all users (pagination)
    @Test
    void testGetAllUsers() {
        List<User> users = List.of(
                new User(1L, "A", "a@test.com", "1234", null, null),
                new User(2L, "B", "b@test.com", "1234", null, null)
        );

        Page<User> page = new PageImpl<>(users);

        when(repo.findAll(any(Pageable.class))).thenReturn(page);

        Page<User> result = service.getAllUsers(PageRequest.of(0, 2));

        assertEquals(2, result.getContent().size());
    }

    //  8. Empty user list
    @Test
    void testGetAllUsersEmpty() {
        Page<User> page = new PageImpl<>(new ArrayList<>());

        when(repo.findAll(any(Pageable.class))).thenReturn(page);

        Page<User> result = service.getAllUsers(PageRequest.of(0, 2));

        assertTrue(result.isEmpty());
    }

    //  9. Verify save called once
    @Test
    void testSaveCalledOnce() {
        User user = new User(null, "Akhila", "a@test.com", "1234", null, null);

        when(repo.save(any())).thenReturn(user);

        service.createUser(user);

        verify(repo, times(1)).save(any());
    }

    //  10. Repository throws exception
    @Test
    void testRepositoryException() {
        User user = new User(null, "Akhila", "a@test.com", "1234", null, null);

        when(repo.save(any())).thenThrow(new RuntimeException("DB error"));

        assertThrows(RuntimeException.class, () -> service.createUser(user));
    }
}