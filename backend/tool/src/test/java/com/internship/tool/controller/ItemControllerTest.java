package com.internship.tool.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.internship.tool.entity.Item;
import com.internship.tool.service.ItemService;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.domain.*;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;
import java.util.List;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
public class ItemControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private ItemService itemService;

    private Item sampleItem() {
        Item item = new Item();
        item.setId(1L);
        item.setName("Test Item");
        item.setDescription("Test Description");
        item.setDeleted(false);
        return item;
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    public void testGetAll_ReturnsOk() throws Exception {
        Page<Item> page = new PageImpl<>(List.of(sampleItem()));
        Mockito.when(itemService.getAll(0, 10, "id", "asc")).thenReturn(page);
        mockMvc.perform(get("/api/items")
                .param("page", "0").param("size", "10")
                .param("sortBy", "id").param("sortDir", "asc"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray());
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    public void testGetById_ReturnsOk() throws Exception {
        Mockito.when(itemService.getById(1L)).thenReturn(sampleItem());
        mockMvc.perform(get("/api/items/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.name").value("Test Item"));
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    public void testCreate_ReturnsOk() throws Exception {
        Mockito.when(itemService.create(Mockito.any())).thenReturn(sampleItem());
        mockMvc.perform(post("/api/items")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(sampleItem())))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Test Item"));
    }

    @Test
    @WithMockUser(roles = "VIEWER")
    public void testCreate_AsViewer_ReturnsForbidden() throws Exception {
        mockMvc.perform(post("/api/items")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(sampleItem())))
                .andExpect(status().isForbidden());
    }

    @Test
    @WithMockUser(roles = "MANAGER")
    public void testUpdate_AsManager_ReturnsOk() throws Exception {
        Mockito.when(itemService.update(Mockito.eq(1L), Mockito.any())).thenReturn(sampleItem());
        mockMvc.perform(put("/api/items/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(sampleItem())))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1));
    }

    @Test
    @WithMockUser(roles = "VIEWER")
    public void testUpdate_AsViewer_ReturnsForbidden() throws Exception {
        mockMvc.perform(put("/api/items/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(sampleItem())))
                .andExpect(status().isForbidden());
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    public void testDelete_AsAdmin_ReturnsNoContent() throws Exception {
        Mockito.doNothing().when(itemService).softDelete(1L);
        mockMvc.perform(delete("/api/items/1"))
                .andExpect(status().isNoContent());
    }

    @Test
    @WithMockUser(roles = "MANAGER")
    public void testDelete_AsManager_ReturnsForbidden() throws Exception {
        mockMvc.perform(delete("/api/items/1"))
                .andExpect(status().isForbidden());
    }

    @Test
    @WithMockUser(roles = "VIEWER")
    public void testSearch_ReturnsOk() throws Exception {
        Page<Item> page = new PageImpl<>(List.of(sampleItem()));
        Mockito.when(itemService.search("Test", 0, 10, "id", "asc")).thenReturn(page);
        mockMvc.perform(get("/api/items/search")
                .param("q", "Test").param("page", "0")
                .param("size", "10").param("sortBy", "id").param("sortDir", "asc"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray());
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    public void testExportCsv_ReturnsOk() throws Exception {
        Mockito.when(itemService.getAllForExport()).thenReturn(List.of(sampleItem()));
        mockMvc.perform(get("/api/items/export"))
                .andExpect(status().isOk())
                .andExpect(header().string("Content-Disposition", "attachment; filename=items.csv"));
    }

    @Test
    public void testGetAll_Unauthenticated_ReturnsUnauthorized() throws Exception {
        mockMvc.perform(get("/api/items"))
                .andExpect(status().isUnauthorized());
    }
}
